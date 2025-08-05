# Wuthering Waves 鳴潮

Damage calculator for Wuthering Waves, analysis of gacha pool records, resource planning, and guide image output. Short-term development will focus on Traditional Chinese, with future consideration for adding multiple languages.

鳴潮傷害計算機、分析抽卡卡池紀錄、資源規劃、攻略圖片輸出。短期開發以繁中為主，未來考慮加入多語系。

專案慢慢地遷移到[WutheringWavesGuideSrc](https://github.com/ZetsuBouKyo/WutheringWavesGuideSrc)，改成以 Javascript 開發，方便直接部署到[攻略網站](https://wutheringwavesguide.netlify.app/)。

## Build

```bash
poetry install
python .\cli.py build --version=<version>
```

## Development

```bash
poetry install
python app.py
```

### Data

The data used in [Wuthering Waves Guide](https://wutheringwavesguide.netlify.app/) can be found at [g/WutheringWavesCache](https://github.com/ZetsuBouKyo/WutheringWavesCache).

The expected folder structure is as follows

```
ww
├── .vscode
├── assets
├── cache
│   └── v1 # https://github.com/ZetsuBouKyo/WutheringWavesCache
├── data
├── docs
├── html
├── tests
├── ww
└── ...
```

## Disclaimer

本網站/本文件所提供的數據分析、計算結果及相關內容均基於玩家社群收集的數據、實驗測試及推測分析，並非來自官方數據或保證準確。

### 數據來源與準確性

- 本分析基於遊戲內測試數據、社群貢獻及公開資訊，可能存在誤差或遺漏。
- 遊戲更新、補丁或平衡調整可能導致數據變動，本網站/本文件不保證即時更新或維持準確性。

### 使用風險

- 本分析結果僅供參考，實際傷害可能因個人操作、武器、聲骸搭配及其他變數而有所不同。
- 玩家應根據自身需求與遊玩體驗作出最佳決策，而非完全依賴本分析內容。

### 與官方無關

- 本網站/本文件與《鳴潮》官方無任何關聯，所有內容均為第三方數據分析與研究。
- 《鳴潮》及相關名稱、圖像、數據均屬原版權方所有，本分析僅供非商業用途參考。

### 最終解釋權

- 本網站/本文件保留對數據分析內容的調整權，若有任何問題，請自行斟酌使用。

## FAQ

https://www.twitch.tv/zetsuboukyo
