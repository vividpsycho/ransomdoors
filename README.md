# JX1DX1

A Windows desktop horror simulation built around JX1DX1. It creates brief, randomized appearances, voice-line title bars, visual glitches, and a timed fragment-collection sequence. The main session window uses the supplied JX1DX1 GIF and all three supplied reference images.

This is an unofficial fan project and is not affiliated with the original creators or Roblox.

## Read before running

The simulation can create and remove its own marker files in configured folders, temporarily change the desktop wallpaper and cursor, and optionally run a shutdown command or custom command if those options are enabled. Those options are off by default. Only run it on a computer you own, review the settings first, and leave command options disabled unless you understand exactly what they do.

The program does not encrypt personal files. Its fragment files are markers used by the simulation. See [LICENSE.md](LICENSE.md) for the project terms.

## Requirements

- Windows x64
- .NET 10 SDK to build from source

## Build

```powershell
dotnet build rans0m.csproj
dotnet run --project rans0m.csproj
```

The published Windows build is self-contained; a separate .NET installation is not required to run it.

## Configuration

Right-click the JX1DX1 system-tray icon and open **JX1DX1 Configuration**. Settings include automatic appearances, delay range, session duration, fragment count, folder mode, and optional failure actions. You can also start a session manually.

## Credits

- JX1DX1 and its associated character/audio belong to their respective original creators. This is an unofficial fan-made project.
- Audio playback uses [NAudio](https://github.com/naudio/NAudio).
- Animated GIF rendering uses [XamlAnimatedGif](https://github.com/XamlAnimatedGif/XamlAnimatedGif).

## License

See [LICENSE.md](LICENSE.md).