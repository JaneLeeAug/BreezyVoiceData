Traceback (most recent call last):
  File "/proj/gpu_mtk53732/do.py", line 3, in <module>
    snapshot_download(
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/modelscope/hub/snapshot_download.py", line 145, in snapshot_download
    return _snapshot_download(
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/modelscope/hub/snapshot_download.py", line 323, in _snapshot_download
    endpoint = _api.get_endpoint_for_read(
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/modelscope/hub/api.py", line 625, in get_endpoint_for_read
    if not self.repo_exists(
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/modelscope/hub/api.py", line 782, in repo_exists
    r = self.session.get(path, cookies=cookies,
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/requests/sessions.py", line 602, in get
    return self.request("GET", url, **kwargs)
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "/proj/MR_dataset/proj/MR_dataset/miniconda3/envs/3dspeaker39/lib/python3.9/site-packages/requests/adapters.py", line 675, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: HTTPSConnectionPool(host='www.modelscope.cn', port=443): Max retries exceeded with url: /api/v1/models/iic/speech_campplus_sv_zh-cn_16k-common (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1147)')))
