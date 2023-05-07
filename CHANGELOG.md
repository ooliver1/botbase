# Changelog

## [2.0.2](https://github.com/ooliver1/botbase/compare/v2.0.1...v2.0.2) (2023-05-07)


### Bug Fixes

* **log-guilds:** actually make them listeners ([7b2ba3a](https://github.com/ooliver1/botbase/commit/7b2ba3a8620675c37ab5ca61697fb819f71898e4))
* **log-guilds:** resolve guild join handler ([a1c0663](https://github.com/ooliver1/botbase/commit/a1c0663efe0639e0f37eb663c50049151a729009))

## [2.0.1](https://github.com/ooliver1/botbase/compare/v2.0.0...v2.0.1) (2023-05-05)


### Bug Fixes

* dont depend on delarva for now ([e3d2a76](https://github.com/ooliver1/botbase/commit/e3d2a769a4214eedf4ceb63cb36d347fb00913ad))

## [2.0.0](https://github.com/ooliver1/botbase/compare/v1.22.3...v2.0.0) (2023-05-05)


### ⚠ BREAKING CHANGES

* [db] is now required as an extra to use database dependencies
* remove unused exceptions mod
* remove guild logging to a cog
* move command logs to a cog
* remove config to kwarg options
* remove emojis dict shim
* remove cli
* use exts/**/*.py for extensions
* remove help config
* **wraps:** remove ctx convert methods
* remove old blacklist
* remove help cog

### Bug Fixes

* add guild ids to delarva ([8acca62](https://github.com/ooliver1/botbase/commit/8acca626e2acbc4e3d0106f3c190c371d355fbf3))
* attempt commandlog composte patch ([1abb10e](https://github.com/ooliver1/botbase/commit/1abb10ef584c59a162a7103638ccc028f4fc049e))
* **blacklist:** i am so good ([622f5e3](https://github.com/ooliver1/botbase/commit/622f5e30c7540b9e6c99f394f8caca4c6cfcdc98))
* **blacklist:** thanks copilot ([13c0933](https://github.com/ooliver1/botbase/commit/13c09332b7db4f2ddd7c2ece12cc450e1e979f97))
* **blacklist:** wait for ready before loading ([f89ddd6](https://github.com/ooliver1/botbase/commit/f89ddd68919c41a83e4d54ea182451ce86383450))
* composite pk? ([7cc0a09](https://github.com/ooliver1/botbase/commit/7cc0a094e82cb9c05e812fde1feda094a9674883))
* import db metadata ([17d263e](https://github.com/ooliver1/botbase/commit/17d263ea4e87e972c390678fd3e827f8298f5b81))
* **log-commands:** i hope ([8a2613a](https://github.com/ooliver1/botbase/commit/8a2613a53732d7eba711011f585bc3bb592f9a2d))
* move db models elsewhere to be cached ([addaf31](https://github.com/ooliver1/botbase/commit/addaf317b27a4633b4e551d25174b58e58a9abc5))
* oh :skull: ([b06e7a5](https://github.com/ooliver1/botbase/commit/b06e7a507711dbf6d4db91961558aa17bb9bb998))
* properly close db ([93a9579](https://github.com/ooliver1/botbase/commit/93a9579d3836b98d97baad0b21e3b505ef2efc46))
* remove import to cogs ([267cbd9](https://github.com/ooliver1/botbase/commit/267cbd9ff42540a719edbbdc1f5efe4102462d21))
* remove unused and outdated checks ([5247d29](https://github.com/ooliver1/botbase/commit/5247d297e742df4c2668834bcfeb1323b692aef2))
* **wraps:** use proper attr for colour from bot ([13b1cfd](https://github.com/ooliver1/botbase/commit/13b1cfd9896021faf7aee1fe4fa3f42476ec3e6a))
* yet again thanks ormar &lt;3 ([2c6f4b4](https://github.com/ooliver1/botbase/commit/2c6f4b4df31c5b9ea8354a2ad9367f110ce7baf1))


### Code Refactoring

* move command logs to a cog ([152c022](https://github.com/ooliver1/botbase/commit/152c0225909c50d5792548d5ae0b883c623697aa))
* remove cli ([f2741d7](https://github.com/ooliver1/botbase/commit/f2741d79b59dceb406057023256948b851da6308))
* remove config to kwarg options ([585377e](https://github.com/ooliver1/botbase/commit/585377e4766996d0a390c5a28b1537fa1635123d))
* remove emojis dict shim ([c07ff54](https://github.com/ooliver1/botbase/commit/c07ff545458ea76e0f2c928dab421f778f8ccbf0))
* remove guild logging to a cog ([c04162d](https://github.com/ooliver1/botbase/commit/c04162dc736a834c140965d8b22968b1d2a851b6))
* remove help cog ([c7a2023](https://github.com/ooliver1/botbase/commit/c7a2023059ccaa8d753df5b2dde3ffcb4779d875))
* remove help config ([79e5469](https://github.com/ooliver1/botbase/commit/79e5469dc2f07a62a407650624073dc16c80b36a))
* remove old blacklist ([dee1ed2](https://github.com/ooliver1/botbase/commit/dee1ed2603ee2bc0626027394defd87063644a26))
* remove unused exceptions mod ([426359d](https://github.com/ooliver1/botbase/commit/426359d2642b54240ae5753f287adb1edb918430))
* use exts/**/*.py for extensions ([14f4dd2](https://github.com/ooliver1/botbase/commit/14f4dd2309794566b19ef6057ae8caf78385cad3))
* **wraps:** remove ctx convert methods ([27f31f0](https://github.com/ooliver1/botbase/commit/27f31f0779c9426f1f967012eb49316944ee477f))


### Miscellaneous Chores

* move db deps to optional extra ([1f97e5b](https://github.com/ooliver1/botbase/commit/1f97e5bacda1ecee3efc3ce5b91c7c8a874c0abf))

## [1.22.3](https://github.com/ooliver1/botbase/compare/v1.22.2...v1.22.3) (2022-10-25)


### Bug Fixes

* **botbase:** support no config at all ([b511ef0](https://github.com/ooliver1/botbase/commit/b511ef0721f695e90c00cc045c43aa3948b36c08))

## [1.22.2](https://github.com/ooliver1/botbase/compare/v1.22.1...v1.22.2) (2022-10-22)


### Bug Fixes

* **botbase:** use str.join because windows ([48554dd](https://github.com/ooliver1/botbase/commit/48554ddd31eefaf19799af546a70a9557b264693))

## [1.22.1](https://github.com/ooliver1/botbase/compare/v1.22.0...v1.22.1) (2022-10-03)


### Bug Fixes

* only sync if ready ([39a752a](https://github.com/ooliver1/botbase/commit/39a752a04d2c1d9991c228e9bb6fdcd8e7b82845))

## [1.22.0](https://github.com/ooliver1/botbase/compare/v1.21.7...v1.22.0) (2022-10-03)


### Features

* add console handlers ([2aff21b](https://github.com/ooliver1/botbase/commit/2aff21b4ef20c4114ee02ba61d15a712c8bcd62f))

## [1.21.7](https://github.com/ooliver1/botbase/compare/v1.21.6...v1.21.7) (2022-10-03)


### Bug Fixes

* istg ([d34b34b](https://github.com/ooliver1/botbase/commit/d34b34bfef0427050d134d2f0f1d151ef930d15a))

## [1.21.6](https://github.com/ooliver1/botbase/compare/v1.21.5...v1.21.6) (2022-10-03)


### Bug Fixes

* oh ([9810669](https://github.com/ooliver1/botbase/commit/9810669d7a85fc015059c47539965146bd455563))

## [1.21.5](https://github.com/ooliver1/botbase/compare/v1.21.4...v1.21.5) (2022-10-03)


### Bug Fixes

* **botbase:** actually fix close and startup ([ab8a243](https://github.com/ooliver1/botbase/commit/ab8a243c58333ae53ac6f0516191177c8bf10149))

## [1.21.4](https://github.com/ooliver1/botbase/compare/v1.21.3...v1.21.4) (2022-09-11)


### Bug Fixes

* **botbase:** support db port ([41bedd1](https://github.com/ooliver1/botbase/commit/41bedd1d2a65ed113065139a6ed6126e7841ca16))

## [1.21.3](https://github.com/ooliver1/botbase/compare/v1.21.2...v1.21.3) (2022-09-10)


### Bug Fixes

* what ([fdf2390](https://github.com/ooliver1/botbase/commit/fdf2390c94b0cb158eec2fb3e6b71c4c9cb75cbb))

## [1.21.2](https://github.com/ooliver1/botbase/compare/v1.21.1...v1.21.2) (2022-09-10)


### Bug Fixes

* **botbase:** cogs are very painful ([1bb9ab9](https://github.com/ooliver1/botbase/commit/1bb9ab918d0d941a15ae85d892ab673e38110b46))

## [1.21.1](https://github.com/ooliver1/botbase/compare/v1.21.0...v1.21.1) (2022-09-10)


### Bug Fixes

* dont import removed emptyembed sentinel ([959fcae](https://github.com/ooliver1/botbase/commit/959fcae2cb99c2cc180726a79f42d09737d9abde))

## [1.21.0](https://github.com/ooliver1/botbase/compare/v1.20.8...v1.21.0) (2022-09-10)


### Features

* **botbase:** add helpers for cogs ([78b2b91](https://github.com/ooliver1/botbase/commit/78b2b91bd3181f4d3ba8a57df262c2806482afcc))

## [1.20.8](https://github.com/ooliver1/botbase/compare/v1.20.7...v1.20.8) (2022-08-02)


### Bug Fixes

* use desc not description pt.2 ([1401519](https://github.com/ooliver1/botbase/commit/1401519b3c38567383b639b0399c4489844ba1aa))

## [1.20.7](https://github.com/ooliver1/botbase/compare/v1.20.6...v1.20.7) (2022-08-02)


### Bug Fixes

* default host to unix instead of host ([9201259](https://github.com/ooliver1/botbase/commit/9201259e7eaa3a44450aef2fb3984d93e7d78c2e))

## [1.20.6](https://github.com/ooliver1/botbase/compare/v1.20.5...v1.20.6) (2022-08-02)


### Bug Fixes

* aaa ([092f131](https://github.com/ooliver1/botbase/commit/092f1315f21636f800d1a46bd0526c1c48fdd83c))

## [1.20.5](https://github.com/ooliver1/botbase/compare/v1.20.4...v1.20.5) (2022-08-02)


### Bug Fixes

* **wraps:** don't use strings for typecast ([337e1f9](https://github.com/ooliver1/botbase/commit/337e1f922fef7aa48a8d6a48bca99e9ff38882e7))

## [1.20.4](https://github.com/ooliver1/botbase/compare/v1.20.3...v1.20.4) (2022-07-27)


### Bug Fixes

* export members properly ([d39453d](https://github.com/ooliver1/botbase/commit/d39453dd6ba92e343f19d3d55638d85c12c9049d))

## [1.20.3](https://github.com/ooliver1/botbase/compare/v1.20.2...v1.20.3) (2022-07-27)


### Bug Fixes

* **wraps:** make bot generic on Context ([0a35940](https://github.com/ooliver1/botbase/commit/0a3594026edffc775e553630600ec5ad4c052721))

## [1.20.2](https://github.com/ooliver1/botbase/compare/v1.20.1...v1.20.2) (2022-07-26)


### Bug Fixes

* add py.typed ([571e090](https://github.com/ooliver1/botbase/commit/571e090147c82b4a85b5233caa5d7739bfc15cd1))

## [1.20.1](https://github.com/ooliver1/botbase/compare/v1.20.0...v1.20.1) (2022-07-17)


### Bug Fixes

* **botbase:** dont ignore errors like that ([d116b04](https://github.com/ooliver1/botbase/commit/d116b0450f6eafd992c0b5fad9c09da07285c26e))

## [1.20.0](https://github.com/ooliver1/botbase/compare/v1.19.2...v1.20.0) (2022-07-10)


### Features

* skip cog files with an underscore ([73739d7](https://github.com/ooliver1/botbase/commit/73739d73eaf0c98218505df38c3a874479b7f166))

## [1.19.2](https://github.com/ooliver1/botbase/compare/v1.19.1...v1.19.2) (2022-07-09)


### Bug Fixes

* seriously use database initialiser ([06aa34f](https://github.com/ooliver1/botbase/commit/06aa34fd1dbc3d63e005cc219130957ed8be43a6))

## [1.19.1](https://github.com/ooliver1/botbase/compare/v1.19.0...v1.19.1) (2022-07-09)


### Bug Fixes

* actually allow empty prefix ([09fb8e1](https://github.com/ooliver1/botbase/commit/09fb8e1110f8a485be16e231197ad452b02eeef8))

## [1.19.0](https://github.com/ooliver1/botbase/compare/v1.18.0...v1.19.0) (2022-07-09)


### Features

* add database initial statement ([5cee930](https://github.com/ooliver1/botbase/commit/5cee930c1b96fa15b4fa15ab4fb149b2be8d6bac))
* use sharded bot ([467505b](https://github.com/ooliver1/botbase/commit/467505b3b036a38d0033a505abb1a0f2250cf073))


### Bug Fixes

* actually allow empty prefix ([97c26ed](https://github.com/ooliver1/botbase/commit/97c26edfed2c24d0cc40832e90fd0e9a5adaa7e2))

## [1.18.0](https://github.com/ooliver1/botbase/compare/v1.17.7...v1.18.0) (2022-07-09)


### Features

* allow no prefix with no database + app event ([ba49928](https://github.com/ooliver1/botbase/commit/ba4992860aa1794bfbcc30f6837f68ef14871185))
* do not load help if no prefix exists ([80bb58b](https://github.com/ooliver1/botbase/commit/80bb58be49269066853a6896771042db5ec971f7))
