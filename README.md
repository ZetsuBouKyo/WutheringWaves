# Wuthering Waves 鳴潮

Damage calculator for Wuthering Waves, analysis of gacha pool records, resource planning, and guide image output. Short-term development will focus on Traditional Chinese, with future consideration for adding multiple languages.

鳴潮傷害計算機、分析抽卡卡池紀錄、資源規劃、攻略圖片輸出。短期開發以繁中為主，未來考慮加入多語系。

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

## FAQ

https://www.twitch.tv/zetsuboukyo
