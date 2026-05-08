import argparse
import os
import sys
import re
from functools import partial
import time
import math

import torch
torch.set_num_threads(1)

import torchaudio
import torchaudio.functional as F
import whisper
import opencc
from hyperpyyaml import load_hyperpyyaml
from huggingface_hub import snapshot_download
from g2pw import G2PWConverter

from cosyvoice.cli.frontend import CosyVoiceFrontEnd
from cosyvoice.cli.model import CosyVoiceModel
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
from cosyvoice.utils.frontend_utils import (
    contains_chinese,
    replace_blank,
    replace_corner_mark,
    remove_bracket,
    spell_out_number,
    split_paragraph,
)
from utils.word_utils import word_to_dataset_frequency, char2phn, always_augment_chars


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/third_party/Matcha-TTS'.format(ROOT_DIR))


def safe_text(x):
    if x is None:
        return ""

    if isinstance(x, float) and math.isnan(x):
        return ""

    text = str(x).strip()

    if text.lower() in ["nan", "none", "null"]:
        return ""

    return text


class CustomCosyVoiceFrontEnd(CosyVoiceFrontEnd):
    def text_normalize_new(self, text, split=False):
        text = safe_text(text)

        if len(text) == 0:
            return "" if split is False else []

        def split_by_brackets(input_string):
            inside_brackets = re.findall(r'\[(.*?)\]', input_string)
            outside_brackets = re.split(r'\[.*?\]', input_string)
            outside_brackets = [part for part in outside_brackets if part]
            return inside_brackets, outside_brackets

        def text_normalize_no_split(text, is_last=False):
            text = safe_text(text)

            if len(text) == 0:
                return ""

            text_is_terminated = text[-1] == "。"

            if contains_chinese(text):
                if self.use_ttsfrd:
                    text = self.frd.get_frd_extra_info(text, 'input')
                else:
                    text = self.zh_tn_model.normalize(text)

                text = safe_text(text)

                if len(text) > 0 and (not text_is_terminated) and (not is_last):
                    text = text[:-1]

                text = text.replace("\n", "")
                text = replace_blank(text)
                text = replace_corner_mark(text)
                text = text.replace(".", "、")
                text = text.replace(" - ", "，")
                text = remove_bracket(text)
                text = re.sub(r'[，,]+$', '。', text)
            else:
                if self.use_ttsfrd:
                    text = self.frd.get_frd_extra_info(text, 'input')
                else:
                    text = self.en_tn_model.normalize(text)

                text = spell_out_number(text, self.inflect_parser)

            return safe_text(text)

        def join_interleaved(outside, inside):
            result = []

            for o, i in zip(outside, inside):
                result.append(o + '[' + i + ']')

            if len(outside) > len(inside):
                result.append(outside[-1])

            return ''.join(result)

        inside_brackets, outside_brackets = split_by_brackets(text)

        for n in range(len(outside_brackets)):
            e_out = text_normalize_no_split(
                outside_brackets[n],
                is_last=(n == len(outside_brackets) - 1),
            )
            outside_brackets[n] = e_out

        text = join_interleaved(outside_brackets, inside_brackets)
        text = safe_text(text)

        if split is False:
            return text

        return [text] if len(text) > 0 else []

    def frontend_zero_shot(self, tts_text, prompt_text, prompt_speech_16k):
        tts_text_token, tts_text_token_len = self._extract_text_token(tts_text)
        prompt_text_token, prompt_text_token_len = self._extract_text_token(prompt_text)

        prompt_speech_22050 = torchaudio.transforms.Resample(
            orig_freq=16000,
            new_freq=22050,
        )(prompt_speech_16k)

        speech_feat, speech_feat_len = self._extract_speech_feat(prompt_speech_22050)
        speech_token, speech_token_len = self._extract_speech_token(prompt_speech_16k)
        embedding = self._extract_spk_embedding(prompt_speech_16k)

        model_input = {
            'text': tts_text_token,
            'text_len': tts_text_token_len,
            'prompt_text': prompt_text_token,
            'prompt_text_len': prompt_text_token_len,
            'llm_prompt_speech_token': speech_token,
            'llm_prompt_speech_token_len': speech_token_len,
            'flow_prompt_speech_token': speech_token,
            'flow_prompt_speech_token_len': speech_token_len,
            'prompt_speech_feat': speech_feat,
            'prompt_speech_feat_len': speech_feat_len,
            'llm_embedding': embedding,
            'flow_embedding': embedding,
        }

        return model_input

    def frontend_zero_shot_dual(
        self,
        tts_text,
        prompt_text,
        prompt_speech_16k,
        flow_prompt_text,
        flow_prompt_speech_16k,
    ):
        tts_text_token, tts_text_token_len = self._extract_text_token(tts_text)
        prompt_text_token, prompt_text_token_len = self._extract_text_token(prompt_text)
        flow_prompt_text_token, flow_prompt_text_token_len = self._extract_text_token(flow_prompt_text)

        flow_prompt_speech_22050 = torchaudio.transforms.Resample(
            orig_freq=16000,
            new_freq=22050,
        )(flow_prompt_speech_16k)

        speech_feat, speech_feat_len = self._extract_speech_feat(flow_prompt_speech_22050)

        flow_speech_token, flow_speech_token_len = self._extract_speech_token(flow_prompt_speech_16k)

        speech_token = flow_speech_token.clone()
        speech_token_len = flow_speech_token_len.clone()

        embedding = self._extract_spk_embedding(prompt_speech_16k)
        flow_embedding = embedding.clone()

        model_input = {
            'text': tts_text_token,
            'text_len': tts_text_token_len,
            'prompt_text': prompt_text_token,
            'prompt_text_len': prompt_text_token_len,
            'llm_prompt_speech_token': speech_token,
            'llm_prompt_speech_token_len': speech_token_len,
            'flow_prompt_speech_token': flow_speech_token,
            'flow_prompt_speech_token_len': flow_speech_token_len,
            'prompt_speech_feat': speech_feat,
            'prompt_speech_feat_len': speech_feat_len,
            'llm_embedding': embedding,
            'flow_embedding': flow_embedding,
        }

        return model_input


class CustomCosyVoiceModel(CosyVoiceModel):
    def __init__(
        self,
        llm: torch.nn.Module,
        flow: torch.nn.Module,
        hift: torch.nn.Module,
    ):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.llm = llm
        self.flow = flow
        self.hift = hift

    def load(self, llm_model, flow_model, hift_model):
        self.llm.load_state_dict(torch.load(llm_model, map_location=self.device))
        self.llm.to(self.device).eval()

        self.flow.load_state_dict(torch.load(flow_model, map_location=self.device))
        self.flow.to(self.device).eval()

        self.hift.load_state_dict(torch.load(hift_model, map_location=self.device))
        self.hift.to(self.device).eval()

    def inference(
        self,
        text,
        text_len,
        flow_embedding,
        llm_embedding=torch.zeros(0, 192),
        prompt_text=torch.zeros(1, 0, dtype=torch.int32),
        prompt_text_len=torch.zeros(1, dtype=torch.int32),
        llm_prompt_speech_token=torch.zeros(1, 0, dtype=torch.int32),
        llm_prompt_speech_token_len=torch.zeros(1, dtype=torch.int32),
        flow_prompt_speech_token=torch.zeros(1, 0, dtype=torch.int32),
        flow_prompt_speech_token_len=torch.zeros(1, dtype=torch.int32),
        prompt_speech_feat=torch.zeros(1, 0, 80),
        prompt_speech_feat_len=torch.zeros(1, dtype=torch.int32),
    ):
        tts_speech_token = self.llm.inference(
            text=text.to(self.device),
            text_len=text_len.to(self.device),
            prompt_text=prompt_text.to(self.device),
            prompt_text_len=prompt_text_len.to(self.device),
            prompt_speech_token=llm_prompt_speech_token.to(self.device),
            prompt_speech_token_len=llm_prompt_speech_token_len.to(self.device),
            embedding=llm_embedding.to(self.device),
            beam_size=1,
            sampling=25,
            max_token_text_ratio=30,
            min_token_text_ratio=3,
        )

        tts_mel = self.flow.inference(
            token=tts_speech_token,
            token_len=torch.tensor(
                [tts_speech_token.size(1)],
                dtype=torch.int32,
            ).to(self.device),
            prompt_token=flow_prompt_speech_token.to(self.device),
            prompt_token_len=flow_prompt_speech_token_len.to(self.device),
            prompt_feat=prompt_speech_feat.to(self.device),
            prompt_feat_len=prompt_speech_feat_len.to(self.device),
            embedding=flow_embedding.to(self.device),
        )

        tts_speech = self.hift.inference(mel=tts_mel).cpu()
        torch.cuda.empty_cache()

        return {'tts_speech': tts_speech}


class CustomCosyVoice:
    def __init__(self, model_dir):
        instruct = False

        if not os.path.isdir(model_dir):
            raise ValueError(
                f"Model path must be a local directory, got: {model_dir}\n"
                "Please download the model beforehand."
            )

        print(f"Using local model path: {model_dir}")
        print("model", model_dir)

        self.model_dir = model_dir

        with open('{}/cosyvoice.yaml'.format(model_dir), 'r') as f:
            configs = load_hyperpyyaml(f)

        self.frontend = CustomCosyVoiceFrontEnd(
            configs['get_tokenizer'],
            configs['feat_extractor'],
            model_dir,
            '{}/campplus.onnx'.format(model_dir),
            '{}/speech_tokenizer_v1.onnx'.format(model_dir),
            '{}/spk2info.pt'.format(model_dir),
            instruct,
            configs['allowed_special'],
        )

        self.model = CosyVoiceModel(configs['llm'], configs['flow'], configs['hift'])

        self.model.load(
            '{}/llm.pt'.format(model_dir),
            '{}/flow.pt'.format(model_dir),
            '{}/hift.pt'.format(model_dir),
        )

        del configs

    def list_avaliable_spks(self):
        spks = list(self.frontend.spk2info.keys())
        return spks

    def inference_sft(self, tts_text, spk_id):
        tts_speeches = []

        for i in self.frontend.text_normalize(tts_text, split=True):
            i = safe_text(i)

            if not len(i):
                continue

            model_input = self.frontend.frontend_sft(i, spk_id)
            model_output = self.model.inference(**model_input)
            tts_speeches.append(model_output['tts_speech'])

        if len(tts_speeches) == 0:
            print(f"[SKIP] No valid text segments in inference_sft. tts_text={repr(tts_text)}")
            return None

        return {'tts_speech': torch.concat(tts_speeches, dim=1)}

    def inference_zero_shot(self, tts_text, prompt_text, prompt_speech_16k):
        prompt_text = self.frontend.text_normalize(prompt_text, split=False)
        tts_speeches = []

        for i in self.frontend.text_normalize(tts_text, split=True):
            i = safe_text(i)

            if not len(i):
                continue

            model_input = self.frontend.frontend_zero_shot(i, prompt_text, prompt_speech_16k)
            model_output = self.model.inference(**model_input)
            tts_speeches.append(model_output['tts_speech'])

        if len(tts_speeches) == 0:
            print(f"[SKIP] No valid text segments in inference_zero_shot. tts_text={repr(tts_text)}")
            return None

        return {'tts_speech': torch.concat(tts_speeches, dim=1)}

    def inference_zero_shot_no_unit_condition_no_normalize(
        self,
        tts_text,
        prompt_text,
        prompt_speech_16k,
        flow_prompt_text=None,
        flow_prompt_speech_16k=None,
    ):
        if flow_prompt_text is None:
            flow_prompt_text = prompt_text

        if flow_prompt_speech_16k is None:
            flow_prompt_speech_16k = prompt_speech_16k

        tts_text = safe_text(tts_text)
        prompt_text = safe_text(prompt_text)

        tts_speeches = []
        segments = re.split(r'(?<=[？！。.?!])\s*', tts_text)

        for i in segments:
            i = safe_text(i)

            if not len(i):
                continue

            model_input = self.frontend.frontend_zero_shot_dual(
                i,
                prompt_text,
                prompt_speech_16k,
                flow_prompt_text,
                flow_prompt_speech_16k,
            )

            print(model_input.keys())

            model_input["llm_prompt_speech_token"] = model_input["llm_prompt_speech_token"][:, :0]
            model_input["llm_prompt_speech_token_len"][0] = 0

            model_output = self.model.inference(**model_input)
            tts_speeches.append(model_output['tts_speech'])

        if len(tts_speeches) == 0:
            print(
                "[SKIP] No valid text segments in "
                f"inference_zero_shot_no_unit_condition_no_normalize. "
                f"tts_text={repr(tts_text)}, segments={[repr(s) for s in segments]}"
            )
            return None

        return {'tts_speech': torch.concat(tts_speeches, dim=1)}

    def inference_zero_shot_no_normalize(self, tts_text, prompt_text, prompt_speech_16k):
        tts_text = safe_text(tts_text)
        prompt_text = safe_text(prompt_text)

        print("[DEBUG] inference_zero_shot_no_normalize tts_text:", repr(tts_text))
        print("[DEBUG] inference_zero_shot_no_normalize prompt_text:", repr(prompt_text))

        tts_speeches = []
        segments = re.split(r'(?<=[？！。.?!])\s*', tts_text)

        print("[DEBUG] split segments:", [repr(s) for s in segments])

        for i in segments:
            i = safe_text(i)

            if not len(i):
                continue

            print("Synthesizing:", i)

            model_input = self.frontend.frontend_zero_shot(
                i,
                prompt_text,
                prompt_speech_16k,
            )

            model_output = self.model.inference(**model_input)
            tts_speeches.append(model_output['tts_speech'])

        if len(tts_speeches) == 0:
            print(
                "[SKIP] No valid text segments in inference_zero_shot_no_normalize. "
                f"tts_text={repr(tts_text)}, segments={[repr(s) for s in segments]}"
            )
            return None

        return {'tts_speech': torch.concat(tts_speeches, dim=1)}


def transcribe_audio(audio_file):
    from transformers import pipeline

    whisper_asr = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-base",
    )

    result = whisper_asr(audio_file)

    converter = opencc.OpenCC('s2t')
    traditional_text = converter.convert(result["text"])

    return traditional_text


def get_bopomofo_rare(text, converter):
    text = safe_text(text)

    if len(text) == 0:
        return ""

    res = converter(text)
    text_w_bopomofo = [x for x in zip(list(text), res[0])]
    reconstructed_text = ""

    for i in range(len(text_w_bopomofo)):
        t = text_w_bopomofo[i]
        char = t[0]
        phn = t[1]

        try:
            next_t_char = text_w_bopomofo[i + 1][0]
        except Exception:
            next_t_char = None

        freq = word_to_dataset_frequency.get(char, 999999999)
        phn_list = char2phn.get(char, [])

        if freq < 500 and phn is not None and next_t_char != '[':
            reconstructed_text += char + f"[:{phn}]"

        elif len(phn_list) >= 2:
            if (
                phn is not None
                and phn != phn_list[0]
                and (freq < 10000 or char in always_augment_chars)
                and next_t_char != '['
            ):
                reconstructed_text += char + f"[:{phn}]"
            else:
                reconstructed_text += char

        else:
            reconstructed_text += char

    return reconstructed_text


def parse_transcript(text, end):
    pattern = r"<\|(\d+\.\d+)\|>([^<]+)<\|(\d+\.\d+)\|>"
    matches = re.findall(pattern, text)

    parsed_output = [
        (float(start), float(end), content.strip())
        for start, content, end in matches
    ]

    count0 = 0

    for i in range(len(parsed_output)):
        if parsed_output[i][0] == 0:
            count0 += 1

        if count0 >= 2:
            parsed_output = parsed_output[:i]
            break

    for i in range(len(parsed_output)):
        if parsed_output[i][0] >= end:
            parsed_output = parsed_output[:i]
            break

    for i in range(len(parsed_output)):
        if parsed_output[i][0] < end - 15:
            continue
        else:
            parsed_output = parsed_output[i:]
            break

    if len(parsed_output) == 0:
        return "", 0

    start = parsed_output[0][0]
    parsed_output = "".join([p[2] for p in parsed_output])

    return parsed_output, start


def single_inference(
    speaker_prompt_audio_path,
    content_to_synthesize,
    output_path,
    cosyvoice,
    bopomofo_converter,
    speaker_prompt_text_transcription=None,
):
    print("=" * 80)
    print("[DEBUG] speaker_prompt_audio_path:", repr(speaker_prompt_audio_path))
    print("[DEBUG] output_path:", repr(output_path))
    print("[DEBUG] raw content_to_synthesize:", repr(content_to_synthesize))
    print("[DEBUG] raw speaker_prompt_text_transcription:", repr(speaker_prompt_text_transcription))

    output_path = safe_text(output_path)

    content_to_synthesize = safe_text(content_to_synthesize)

    if len(content_to_synthesize) == 0:
        print(f"[SKIP] Empty content_to_synthesize. output_path={repr(output_path)}")
        return False

    prompt_speech_16k = load_wav(speaker_prompt_audio_path, 16000)

    if speaker_prompt_text_transcription:
        speaker_prompt_text_transcription = safe_text(speaker_prompt_text_transcription)
    else:
        speaker_prompt_text_transcription = transcribe_audio(speaker_prompt_audio_path)

    speaker_prompt_text_transcription = safe_text(speaker_prompt_text_transcription)

    if len(speaker_prompt_text_transcription) == 0:
        print(
            "[SKIP] Empty speaker_prompt_text_transcription. "
            f"speaker_prompt_audio_path={repr(speaker_prompt_audio_path)}, "
            f"output_path={repr(output_path)}"
        )
        return False

    converter = opencc.OpenCC('s2t')

    try:
        speaker_prompt_text_transcription_norm = cosyvoice.frontend.text_normalize_new(
            speaker_prompt_text_transcription,
            split=False,
        )

        content_to_synthesize_norm = cosyvoice.frontend.text_normalize_new(
            content_to_synthesize,
            split=False,
        )

        speaker_prompt_text_transcription_norm = converter.convert(
            safe_text(speaker_prompt_text_transcription_norm)
        )

        content_to_synthesize_norm = converter.convert(
            safe_text(content_to_synthesize_norm)
        )

    except Exception as e:
        print(
            "[SKIP] text_normalize_new failed. "
            f"output_path={repr(output_path)}, "
            f"content={repr(content_to_synthesize)}, "
            f"prompt_text={repr(speaker_prompt_text_transcription)}, "
            f"error={repr(e)}"
        )
        return False

    print("[DEBUG] normalized speaker_prompt_text_transcription:", repr(speaker_prompt_text_transcription_norm))
    print("[DEBUG] normalized content_to_synthesize:", repr(content_to_synthesize_norm))

    if len(safe_text(content_to_synthesize_norm)) == 0:
        print(
            "[SKIP] content_to_synthesize became empty after normalization. "
            f"raw={repr(content_to_synthesize)}, "
            f"output_path={repr(output_path)}"
        )
        return False

    if len(safe_text(speaker_prompt_text_transcription_norm)) == 0:
        print(
            "[SKIP] speaker_prompt_text_transcription became empty after normalization. "
            f"raw={repr(speaker_prompt_text_transcription)}, "
            f"output_path={repr(output_path)}"
        )
        return False

    try:
        speaker_prompt_text_transcription_bopomo = get_bopomofo_rare(
            speaker_prompt_text_transcription_norm,
            bopomofo_converter,
        )

        content_to_synthesize_bopomo = get_bopomofo_rare(
            content_to_synthesize_norm,
            bopomofo_converter,
        )

    except Exception as e:
        print(
            "[SKIP] get_bopomofo_rare failed. "
            f"output_path={repr(output_path)}, "
            f"content_norm={repr(content_to_synthesize_norm)}, "
            f"prompt_norm={repr(speaker_prompt_text_transcription_norm)}, "
            f"error={repr(e)}"
        )
        return False

    print("Speaker prompt audio transcription:", repr(speaker_prompt_text_transcription_bopomo))
    print("Content to be synthesized:", repr(content_to_synthesize_bopomo))

    if len(safe_text(content_to_synthesize_bopomo)) == 0:
        print(
            "[SKIP] content_to_synthesize became empty after bopomofo conversion. "
            f"normalized={repr(content_to_synthesize_norm)}, "
            f"output_path={repr(output_path)}"
        )
        return False

    if len(safe_text(speaker_prompt_text_transcription_bopomo)) == 0:
        print(
            "[SKIP] speaker_prompt_text_transcription became empty after bopomofo conversion. "
            f"normalized={repr(speaker_prompt_text_transcription_norm)}, "
            f"output_path={repr(output_path)}"
        )
        return False

    start = time.time()

    try:
        output = cosyvoice.inference_zero_shot_no_normalize(
            content_to_synthesize_bopomo,
            speaker_prompt_text_transcription_bopomo,
            prompt_speech_16k,
        )

    except Exception as e:
        print(
            "[SKIP] inference_zero_shot_no_normalize failed. "
            f"output_path={repr(output_path)}, "
            f"content_bopomo={repr(content_to_synthesize_bopomo)}, "
            f"prompt_bopomo={repr(speaker_prompt_text_transcription_bopomo)}, "
            f"error={repr(e)}"
        )
        return False

    if output is None:
        print(
            "[SKIP] Inference returned None. "
            f"output_path={repr(output_path)}, "
            f"content_bopomo={repr(content_to_synthesize_bopomo)}"
        )
        return False

    end = time.time()

    print("Elapsed time:", end - start)
    print("Generated audio length:", output['tts_speech'].shape[1] / 22050, "seconds")

    torchaudio.save(output_path, output['tts_speech'], 22050)

    print(f"Generated voice saved to {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Run BreezyVoice text-to-speech with custom inputs"
    )

    parser.add_argument(
        "--content_to_synthesize",
        type=str,
        required=True,
        help="Specifies the content that will be synthesized into speech.",
    )

    parser.add_argument(
        "--speaker_prompt_audio_path",
        type=str,
        required=True,
        help="Specifies the path to the prompt speech audio file of the speaker.",
    )

    parser.add_argument(
        "--speaker_prompt_text_transcription",
        type=str,
        required=False,
        help="Specifies the transcription of the speaker prompt audio.",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        required=False,
        default="results/output.wav",
        help="Specifies the name and path for the output .wav file.",
    )

    parser.add_argument(
        "--model_path",
        type=str,
        required=False,
        default="MediaTek-Research/BreezyVoice-300M",
        help="Specifies the model used for speech synthesis.",
    )

    args = parser.parse_args()

    cosyvoice = CustomCosyVoice(args.model_path)

    bopomofo_converter = G2PWConverter(
        model_dir="../g2pw",
    )

    single_inference(
        speaker_prompt_audio_path=args.speaker_prompt_audio_path,
        content_to_synthesize=args.content_to_synthesize,
        output_path=args.output_path.strip(),
        cosyvoice=cosyvoice,
        bopomofo_converter=bopomofo_converter,
        speaker_prompt_text_transcription=args.speaker_prompt_text_transcription,
    )


if __name__ == "__main__":
    main()
