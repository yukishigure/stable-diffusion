# Optimized Stable Diffusion

本リポジトリは、[@basujindal](https://github.com/basujindal)氏による[Optimized Stable Diffusion](https://github.com/basujindal/stable-diffusion)のフォーク版です。  
[Optimized Stable Diffusion GUI Tool](https://booth.pm/ja/items/4118603)での操作に最適化するための機能追加や、変更を行っています。  
また、GUI Toolとの連携を意識して開発を進めていますが、他のStable Diffusionのリポジトリと同様、CUIで実行することも可能です。  

# yukishigure版の特徴
- Optimized Stable Diffusionからのフォークのため、4GB以下のVRAM環境でも動作
- Seamless Texture対応
- 日本語prompt対応

# コマンド
## `--translate`  
promptに英語以外の言語を使用することが出来ます。  

### 引数  
- `--translate ja`  
promptを日本語から英語に翻訳します

### デフォルト値
`None`

## `--seamless`
シームレスな画像を出力することが出来ます

### 引数
- `--seamless reflect`  
各辺で反転させて配置することを想定したシームレス画像を出力します  

- `--seamless circular`  
敷き詰めて配置することを想定したシームレス画像を出力します

### デフォルト値
`None`


# 本家README
[optimizedSD/README.md]("optimizedSD/README.md")