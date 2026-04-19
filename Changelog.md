# Changelog

All notable changes to the **Matrial Asset Browser** will be documented in this file.

## [0.0.20] - 2026-04-19

### ✨ New Features
* **Folder Tree View:** Integrated a hierarchical folder panel on the left for faster navigation, complete with a dedicated toolbar toggle button.
* **Persistent Caching & Database:** Implemented a `material_db.json` file within the root material folder. This allows for near-instant (In-Memory) searching across thousands of assets and significantly speeds up initial load times.
* **Intelligent Tagging System:**
    * Users can now add custom tags to any material via the right-click context menu.
    * Features a modern **Pill/Chip UI** for tag management with quick-delete (×) functionality and Enter-to-add support.
* **Hybrid Search Engine:** The search bar now indexes both material names and assigned tags, making asset discovery much more intuitive.
* **Library Portability:** Since the tag database is stored within the material root, the library remains portable; tags and metadata are preserved when moving the library to different drives or systems.

### 🛠 Improvements & Bug Fixes
* **Synchronized Rename Logic:** Completely refactored the rename function. Renaming a material now simultaneously updates the physical `.mat` file, the `.jpg` thumbnail, and the database record.
* 🎨 UI/UX Enhancements:**
    * **Input Boxes:** Improved color contrast in Dark Mode for better accessibility.
    * **Tag Chips:** Refined alignment and rounded the edges of delete buttons for a cleaner aesthetic.
    * **Status Bar:** Fixed the vertical stretching issue when using the `QSplitter`.
* **Modular Code Architecture:** Separated styles and auxiliary dialogs into dedicated files (`style.py` and `TagManagerDialog.py`), resulting in a cleaner `ui.py` and easier maintenance.
* **Smart Refresh System:** The **Refresh** button now supports a "Force Rescan" mode to detect manual file changes on the disk without losing existing tag data.


## [0.0.18] - 2026-02-26

### 🎨 UI/UX Enhancements
* **Centralized Color System:** Converted all hardcoded hex colors in `style.py` into centralized variables, paving the way for easier theme management and a unified visual language.
* **Optimized Card Spacing:** Reduced redundant margins and padding on material cards, resulting in a cleaner, tighter grid layout without dead space.
* **Smart Responsive Layout:** Enabled fluid wrapping (`QListWidget.Adjust`); material cards now dynamically reorganize themselves seamlessly when resizing the browser window inside 3ds Max.

### 🛠 Stability & Bug Fixes
* **Scroll Jump Fix (Lazy Loading):** Implemented a state-save mechanism for the vertical scrollbar. Loading new batches of materials no longer resets the scroll position to the top, providing a seamless and uninterrupted browsing experience.
* **UI Engine Stabilization:** Restored strict `GridSize` dimensions alongside the responsive mode. This prevents the Qt engine from redundantly recalculating item sizes during batch loads, completely eliminating UI lag and stuttering in massive material libraries.

## [0.0.17] - 2026-02-23

### 🚀 Performance & Loading Optimization
* **Lazy Loading Implementation:** Introduced `BatchLoader` to process materials in chunks of 10 items, preventing 3ds Max from freezing in large libraries.
* **Smart Scroll Loading:** Integrated the loader with the `asset_list` vertical scrollbar; additional items now load dynamically as the user scrolls down.
* **Optimized Folder Parsing:** Re-engineered the `load_folder` logic to handle directory navigation and `.mat` file processing separately for near-instant folder opening.

### 🛠 Stability & Bug Fixes
* **AttributeError Resolution:** Fixed a critical crash in the `__init__` method by reordering widget creation, ensuring `asset_list` exists before the loader attempts to bind to it.
* **Module Path Isolation:** Overhauled `launch.py` to intelligently manage `sys.path`, preventing conflicts with other Python-based tools (e.g., OpenKitbash).
* **Constants Integrity:** Fixed "Missing Attribute" errors by unifying all global variables (Paths, Titles, Versions) within a dedicated `constants.py` module.
* **Docking Fix:** Corrected the `setFloating` behavior in the launch sequence to ensure the UI properly snaps to the 3ds Max right-hand dock area.

### 🎨 UI/UX Enhancements
* **New Settings Dialog:** Migrated configuration settings to a standalone `settings_dialog.py` file, featuring a modern GroupBox-based layout.
* **Professional "About" Section:** Added a centralized product info area with direct links to **GitHub** via `QDesktopServices` for better stability within Max.
* **Status Bar Feedback:** Implemented color-coded status messages to guide users through the batch loading process.

### 🧹 Code Refactoring
* **Legacy Cleanup:** Removed redundant `SettingsDialog` classes and dead methods from `logic.py` and `ui.py` to improve maintainability.
* **Resource Management:** Optimized the way icons and thumbnails are checked and loaded to reduce memory overhead.

---
*Developed with ❤️ by Iman Shirani*
