[app]

title = HotelBruno
package.name = hotelbruno
package.domain = org.hotelbruno
source.dir = .
source.main = main.py

source.include_exts = py,kv,png,jpg,ttf,atlas

version = 1.0.0

requirements = python3,kivy==2.3.1,kivymd,requests
verbose = 1

#esto seria vertical
orientation = portrait 

fullscreen = 0

# aca empieza la parte de android
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 24

android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

android.copy_libs = 1

android.logcat_filters = *:S python:D

android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0


# parte de ios
osx.kivy_version = 2.3.1
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.codesign.allowed = false
p4a.num_jobs = 1

[buildozer]
log_level = 2
warn_on_root = 1