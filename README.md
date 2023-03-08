# 6TRON Flash

Tool to flash 6TRON boards.

## Install

### Pip

With `pip`, install with:

```shell
python3 -m pip install git+https://github.com/catie-aq/6tron_flash.git#egg=sixtron_flash
```

### Pipx

[Pipx](https://pypa.github.io/pipx/) allows to install and run Python applications in
isolated environments.

With `Pipx`, install with:

```shell
pipx install git+https://github.com/catie-aq/6tron_flash.git#egg=sixtron_flash
```

## Usage

```shell
Usage: sixtron_flash [OPTIONS] [JLINK_DEVICE] [FILE_PATH]

  Console tool to flash 6TRON boards.

Options:
  --help                        Show this message and exit.
```

## 6TRON Boards

| Board                 | Target                | JLink device  |
| --------------------- | --------------------- | ------------- |
| Z_Environment         | Z_ENVIRONMENT         | stm32l496rg   |
| Z_Motion              | Z_MOTION              | stm32l496rg   |
| Zest_Core_FMLR-72     | ZEST_CORE_FMLR-72     | stm32l071rz   |
| Zest_Core_MTXDOT      | ZEST_CORE_MTXDOT      | stm32l151cc   |
| Zest_Core_STM32G474VE | ZEST_CORE_STM32G474VE | stm32g474ve   |
| Zest_Core_STM32H753ZI | ZEST_CORE_STM32H753ZI | STM32h753zi   |
| Zest_Core_STM32L496RG | ZEST_CORE_STM32L496RG | stm32l496rg   |
| Zest_Core_STM32L496ZG | ZEST_CORE_STM32L496ZG | stm32l496zg   |
| Zest_Core_STM32L4A6RG | ZEST_CORE_STM32L4A6RG | stm32l4a6rg   |
| Zest_Core_STM32L562VE | ZEST_CORE_STM32L562VE | stm32l562ve   |
| Zest_Core_nRF52832    | ZEST_CORE_NRF52832    | nrf52832_xxaa |
