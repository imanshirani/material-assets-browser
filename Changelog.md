# Changelog

All notable changes to the **Material Asset Browser** will be documented in this file.

## [0.0.22] - 2026-08-13 🚀 Release

### ✨ New Features
* **Drag & Drop to Viewport:** Materials can now be dragged directly from the browser and dropped onto any mesh object in the 3ds Max viewport to instantly assign them. A floating label follows the cursor during drag, showing the material name. The cursor changes to a forbidden icon when hovering outside a valid viewport, and pressing Escape cancels the operation.

### 🛠 Bug Fixes
* **Crash Fix — `SettingsDialog`:** Removed a duplicate `SettingsDialog` class in `logic.py` that defined a `create_about_tab()` call without implementing the method, causing an immediate crash on open.
* **Crash Fix — `QColor` missing import:** `add_folder_item` was calling `QColor` without importing it, crashing whenever a folder had no icon file.
* **Crash Fix — `shutil` missing import:** `move_material_to_folder` was using `shutil.move` without importing `shutil`.
* **Crash Fix — `original_renderer` in `finally`:** In `generate_thumbnail`, if `pymxs` failed to import, the `finally` block would raise a `NameError` on `original_renderer`. Variable is now initialized to `None` before the `try` block.
* **AttributeError — `self.context_menu`:** Used in `move_material_to_folder` before ever being assigned. Added initialization in `__init__`.
* **Layout Bug — `search_bar` added twice:** `search_bar` was added to both `tools_layout` and `main_layout`. Qt silently moves the widget to the second layout, leaving `group_tools` missing it. Fixed by keeping only the `main_layout` placement.
* **Silent error swallow in `load_config`:** Bare `except: pass` was hiding all config-load failures. Changed to `except Exception as e` with a logged message.
* **CSS syntax error in `style.py`:** `TAG_LIST_STYLE` had a trailing `/` after a CSS property, breaking the stylesheet silently.
* **Duplicate imports in `logic.py`:** `QLabel` and `QVBoxLayout` were listed twice in the same `from PySide6.QtWidgets import` block.
* **Redundant `CONFIG_PATH` assignment:** An intermediate assignment to `CONFIG_PATH` in `logic.py` was immediately overwritten on the next line — removed.
* **Redundant `setDragEnabled(False)`** called twice in sequence on `asset_list` — duplicate removed.

### 🧹 Code Cleanup
* Removed dead functions `find_3dsmaxcmd` and `find_octane_max` from `logic.py` (defined but never called).
* Removed dead `write_maxscript` method from `ui.py` (was replaced by in-process rendering in an earlier version).
* Removed unused imports from `logic.py`: `uuid`, `tempfile`, `subprocess`, `inspect`, `platform`, `deque`, `Counter`, `import style`.
* Removed redundant `importlib.reload()` calls in `MaterialAssetsBrowser.py` — deleting a module from `sys.modules` and then importing it is already a fresh load; reloading again immediately after was a no-op.
* Simplified `is_mat` detection in `show_context_menu` from a complex `endswith` chain to a readable `split("::")[0].endswith(".mat")`.
* Removed unused `self.asset_list.selectedItems()` call (result was discarded).

---

## [0.0.21] - 2026-06-07

### ✨ New Features
* Automated Background Thumbnail Queuing: Integrated an intelligent lazy-loading thumbnail generation system. When navigating into a directory, the browser automatically scans for assets missing thumbnails and queues them for background rendering without blocking or freezing the 3ds Max main thread UI.

* Universal OpenPBR Material Generation: Refactored the automated PBR texture import pipeline to generate standardized OpenPBR_Material nodes instead of legacy engine-specific wrappers (Std_Surface_Mtl). Materials created through the pipeline are now natively portable across all major production renderers (V-Ray, Arnold, Corona, Redshift, and Octane).

* Multi-Select Batch Rendering: Enhanced the asset list context menu to support multi-selection. Users can now select multiple material assets simultaneously and trigger the "Generate Thumbnail" command to batch-populate the background render queue.

### 🛠 Improvements & Bug Fixes
* Robust Path Normalization: Hardened the material loading subsystem in ui.py using os.path.normpath and unified slash handling. This prevents Python exceptions and silent crashes when parsing inconsistent Windows backslashes (\) or missing file indicators.

* Smarter PBR Texture Identification: Rewrote the mapping algorithm (find_map) to utilize a robust 3-stage heuristic priority chain. The updated engine successfully ignores resolution strings (e.g., _4k, -8k) and eliminates token conflicts—such as mistakenly identifying an Albedo map as a Metalness map when the base asset string contains overlapping keyword criteria.

* Synchronized Library Paths: Fixed a critical path-saving bug in the PBR generation module. Generated .mat material libraries are now written directly to the active texture source directory rather than falling back to the global material root.


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
