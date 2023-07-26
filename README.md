# Optimized Stable Diffusion

本リポジトリは、[@basujindal](https://github.com/basujindal)氏による[Optimized Stable Diffusion](https://github.com/basujindal/stable-diffusion)を@yukishigure版として新たにフォークしたものです。  
[Optimized Stable Diffusion GUI Tool](https://booth.pm/ja/items/4118603)での操作に最適化するための機能追加や、変更、バグ修正などを行っています。  
また、GUI Toolとの連携を意識して開発を進めていますが、他のStable Diffusionのリポジトリと同様、CUIで実行することも可能です。  

# yukishigure版の特徴
- Optimized Stable Diffusionからのフォークのため、2.4GB以下のVRAM環境でも512x512解像度の画像出力が可能
- Seamless Texture対応
- 日本語Prompt対応
- NegativePrompt対応
- 8種類のSamplerに対応（※img2imgは7種類）

# 引数
## `--translate`  
promptに英語以外の言語を使用することが出来ます。  

### バリエーション  
- `--translate ja`  
promptを日本語から英語に翻訳します

### デフォルト値
`None`  
  
## `--seamless`
シームレスな画像を出力することが出来ます

### バリエーション
- `--seamless reflect`  
各辺で反転させて配置することを想定したシームレス画像を出力します  

- `--seamless circular`  
敷き詰めて配置することを想定したシームレス画像を出力します  

### デフォルト値  
`None`  
  
## `--ckpt`  
使用するモデルファイル(.ckptファイル)を変更します  

### バリエーション  
- `--ckpt [ファイルパス]`  
使用するモデルを、ファイルパスで指定したckptファイルで上書きします  

### デフォルト値  
`models/ldm/stable-diffusion-v1/model.ckpt`
  
# 本家README  
[optimizedSD/README.md](optimizedSD/README.md)
