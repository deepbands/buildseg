# 设置1张可用的卡
# export CUDA_VISIBLE_DEVICES=0  # linux / macos
set CUDA_VISIBLE_DEVICES=0  # windows

# 导出
python export.py --config ocrnet_hrnet_w18_512x512.yml \
	--model_path ocrnet_hrnet_w18_512x512_rs_building.pdparams \
	--save_dir static_weight