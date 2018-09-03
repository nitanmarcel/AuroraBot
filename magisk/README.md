# Minimal Aurora Store Installer
### By Whyorean (scripting by FriendlyNeighborhoodShane)
*A simple, flexible Aurora Installer with just the essentials*

### Links
* [GitHub](https://github.com/NoGooLag/Aurora_Packs)
* [Support](https://t.me/joinchat/INQp0kX2D7fcxcAXY6eZJA)
### Description
This is a simple Aurora installer. It can install Aurora into your system partition or as a Magisk module. It supports virtually all mobile architectures (arm/64, x86/64, mips/64) but Aurora Store only supports Lollipop and above. It can even uninstall itself from your device, just rename it and flash it again.

For support:
If you flashed through recovery, provide its logs.
If you used Magisk Manager, provide its logs.

How to control the zip by changing its name:
NOTE: Control by name is not possible in magisk manager, since it copies the zip to a cache directory and renames it install.zip. This is unavoidable behaviour.

1. Add 'system' to its filename to force it to install/uninstall from system. Otherwise, it looks for magisk, and if not found, installs to system. Obviously, if you flash it through Magisk manager, you want to install it to Magisk. If not, you have to flash through recovery.

2. Add 'uninstall' to its filename to uninstall it from your device, whether in magisk mode or system mode. If you use Magisk Manager, your preffered method of uninstallation is from there.

3. You can create you own config of what should be installed by the zip. Just check the 'EXAMPLE-MinMicroG-conf.sh' file for instructions. To use this from Magisk manager, you have to put it in /sdcard/MinMicroG.

Just rename it and flash it again for the intended effect.

Thanls to @osm0sis for the base magisk/recovery code and inspiration and guidance on the majority of the stuff in here. You're awesome.
Thanks to @Setialpha, the creator of NanoDroid, and ale5000 for the lib installation code and permissions code.
