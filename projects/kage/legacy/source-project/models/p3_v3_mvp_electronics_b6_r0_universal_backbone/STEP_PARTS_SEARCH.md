# B6-R0 step.parts search record

Search date: 2026-08-20. Canonical API `https://api.step.parts/v1/parts` was reachable. Catalog response reported 16,847 parts and catalog SHA-256 `36766ef8cf73776fd12d659855ec9de51527e29c4d10d1d752b84df8153a593b`.

No catalog STEP was used for a board-specific mount pattern. The MVP keeps all electronics interfaces as universal 3.4 x 12 mm radial slots with ordinary side-loaded M3 nuts.

## Exact-name and alias results

- Waveshare ESP32-C6 Touch LCD: no match. Also searched `ESP32-C6 Touch LCD`, `ESP32 C6 LCD`, `Waveshare ESP32-C6`, `Waveshare Touch LCD`, `Waveshare ESP32-C6-Touch-LCD-1.47`, `ESP32-C6-Touch-LCD-1.47`, and `ESP32-C6 LCD 1.47`; all returned zero.
- NEMA 8 reference: `NEMA 8` returned NEMA08 analytic simplified references. The nearest length is `stepper_motor_nema08_l0040_single_shaft`, 20.3 mm frame, 16 mm bolt spacing, 4 mm shaft, 40 mm body, SHA-256 `534300417337aca800ef32b41f97df3b6b8b39373d4d112c2a1d5151af9302ea`. This is a near match, not the confirmed 39.3 mm handoff envelope. `NEMA08 39.3`, `NEMA 8 39`, `20HS stepper`, and `20mm stepper motor` returned zero.
- TMC2209 carriers: no match. Searched `TMC2209 carrier`, `TMC2209 stepper driver`, `BIGTREETECH TMC2209`, `BTT TMC2209`, `Pololu TMC2209`, `TMC 2209`, `SilentStepStick TMC2209`, and `Trinamic TMC2209`.
- USB-C PD trigger: no match. Searched `USB-C PD trigger`, `USB C PD decoy`, `PD trigger module`, `Type-C PD trigger`, `ZY12PDN`, `HW-398 PD`, `PD decoy`, and `USB PD sink trigger`.
- 12V-to-5V buck: no exact selected-board match. Generic candidates were `power_control_module_lm2596_buck_module`, SHA-256 `9c7db0f3060d7aa773826bf0c180eb32b8a26642c1851b9c3cc9def618351ed2`, and `power_control_module_mp1584_buck_module`, SHA-256 `e779e960d5ef50b9cd3c65cc6a7334613c58236cdacc1c4bee87bf4ee202d9e9`. Searches `12V 5V buck converter`, `12V-to-5V buck`, and `DC DC converter 12V 5V` returned zero. Neither generic module is treated as the selected board.
- LED constant-current driver: no match. Searched `LED constant current driver`, `350mA LED driver`, `BuckPuck 350mA`, `constant-current LED module`, `CC LED driver`, `LDD-350L`, `Mean Well LDD 350`, `PicoBuck 350`, `PT4115 module`, and `350 mA constant current`.

## Resulting envelope policy

Confirmed references remain R4 and the handoff NEMA 8 envelope only. Replaceable variables remain exactly `esp_env_xyz=(50,40,15)`, `tmc_env_xyz=(22,18,15)`, `pd_trigger_env_xyz=(30,20,10)`, `logic_buck_env_xyz=(45,25,15)`, `led_cc_driver_env_xyz=(45,25,15)`, and `installed_height_max=15`.
