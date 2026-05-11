from modelscope import snapshot_download

snapshot_download(
    "iic/speech_campplus_sv_zh-cn_16k-common",
    cache_dir="/proj/MR_dataset/mtk53732/3dspeaker/modelscope_cache"
)
