# Android APK wrapper

1. Deploy the Django site to an HTTPS address.
2. In `app/build.gradle`, replace `https://example.com/` in `SITE_URL` with that address.
3. Open this `android-wrapper` folder in Android Studio.
4. Select **Build → Build APK(s)**. Android Studio creates `app-debug.apk`, which can be copied to an Android phone and installed.

The app is a secure WebView wrapper around the deployed site. The site must be online for dynamic Django pages and API calls to work.
