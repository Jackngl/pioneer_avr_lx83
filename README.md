# Pioneer AVR LX83 Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/Jackngl/pioneer_avr_lx83.svg)](https://GitHub.com/Jackngl/pioneer_avr_lx83/releases/)
[![License](https://img.shields.io/github/license/Jackngl/pioneer_avr_lx83.svg)](LICENSE)

Custom Home Assistant integration for Pioneer AVR LX83 receivers using Telnet protocol.

## Features

- ✅ Power on/off control
- ✅ Volume control (set, up, down)
- ✅ Mute/unmute
- ✅ Source selection
- ✅ Real-time status updates
- ✅ Config flow UI configuration
- ✅ HACS compatible

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/Jackngl/pioneer_avr_lx83` as repository
6. Select "Integration" as category
7. Click "Add"
8. Search for "Pioneer AVR LX83" and install

### Manual Installation

1. Copy the `custom_components/pioneer_avr_lx83` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration"
3. Search for "Pioneer AVR LX83"
4. Enter your device's IP address, port (default: 23), and a name
5. Click "Submit"

## Supported Sources

- CD
- Tuner
- Phono
- DVD
- TV/Sat
- DVR/BDR
- Video
- iPod/USB
- NET

## Telnet Commands

The integration uses the following Telnet commands:

| Command | Description |
|---------|-------------|
| `PO` | Power On |
| `PF` | Power Off |
| `?P` | Query Power State |
| `VLxxx` | Set Volume (000-185) |
| `?V` | Query Volume |
| `MO` | Mute On |
| `MF` | Mute Off |
| `?M` | Query Mute State |
| `FNxx` | Select Source |
| `?F` | Query Source |

## Troubleshooting

### Cannot connect to device

- Verify the IP address is correct
- Ensure Telnet is enabled on your Pioneer AVR
- Check that port 23 is not blocked by a firewall
- Verify the device is on the same network

### Device not responding

- Restart the Pioneer AVR
- Restart Home Assistant
- Check network connectivity

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by Jack

## Support

If you encounter any issues, please [open an issue](https://github.com/Jackngl/pioneer_avr_lx83/issues) on GitHub.

