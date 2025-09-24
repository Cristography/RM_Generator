# RM_Generator⌚

**RM_Generator** is a generative art engine designed to create stunning, programmatically colored collections from layered artwork. Inspired by the avant-garde design and technical artistry of Richard Mille timepieces, this tool transforms your component PNGs into thousands of unique, beautifully harmonized variations.

Think of it as a digital watchmaker's bench. You provide the components (the layers), and MilleGenesis assembles and finishes each unique piece with a master's eye for color.

<img width="690" height="764" alt="image" src="https://github.com/user-attachments/assets/d7a48c62-7785-4f05-a9a2-8248abcb91e3" />

<img width="1616" height="811" alt="image" src="https://github.com/user-attachments/assets/ae768ce5-60c6-494c-8969-596a72422bc8" />


* * *

## ⚙️ Core Mechanics (Features)

* **Horological Color Harmonies:** Palettes are not random. They are generated using color theory principles (Triadic, Complementary, etc.) to ensure every piece is a masterwork of aesthetic balance, just like a well-designed timepiece.
* **The "Turbillon" of Creativity:** A "Temperature" slider acts as the creative escapement of the engine. Low settings produce disciplined, elegant palettes. High settings introduce controlled chaos for bold, experimental, and avant-garde results.
* **Deterministic Assembly (Seeding):** Discover a "pièce unique"? Use the `Seed` function to perfectly replicate any generation, ensuring your favorite combinations are never lost to time.
* **Layered Construction:** Faithfully mimics the layered complexity of a watch dial. The program stacks, colorizes, and merges your transparent PNG layers into a final, intricate composite.
* **Modern Workshop (GUI):** The sleek CustomTkinter interface provides a clean, modern workspace that feels right at home on any OS, with automatic light/dark mode support.
* **Haute Horlogerie Production:** Effortlessly generate collections of any size, from a limited edition run of 10 to a grand complication of 10,000.

* * *

## 🚀 Getting Started

To get the MilleGenesis engine running, follow these steps.

### Prerequisites

You must have Python 3 installed on your system.

### Installation

1. **Clone the repository:**
  
      git clone https://github.com/your-username/MilleGenesis.git
      cd MilleGenesis
  
2. **Install dependencies from `requirements.txt`:**
  
      pip install -r requirements.txt
  
  *(Note: Ensure you have a `requirements.txt` file in your repository with the following content:)*
  
      Pillow
      customtkinter
      matplotlib
  

### Launching the Engine

With the dependencies installed, launch the application:

    python RM_Generator.py

* * *

## 🛠️ The Watchmaker's Guide (How to Use)

Follow this process to craft your first collection.

1. **Prepare the Components (Asset Structure):**
  
  * Create a folder for your input assets. Inside, place your watch layers as transparent PNGs.
  * **Crucially, the layers are stacked in alphabetical/numerical order.** The first file alphabetically (`0_base.png` or `case.png`) will be the bottom layer. The last file (`9_hands.png` or `screws.png`) will be the top layer.
  * All PNGs should have the same dimensions.
  
  Example structure:
  
      my_watch_assets/
      ├── 0_case.png
      ├── 1_dial_base.png
      ├── 2_numbers.png
      ├── 3_gears.png
      └── 4_hands.png
  
2. **Select Folders:**
  
  * **Input Folder:** Select the `my_watch_assets` folder.
  * **Output Folder:** Choose an empty folder to save your finished collection.
3. **Set Production Parameters:**
  
  * **Number to Generate:** The size of your collection.
  * **Output Filename Base:** A name for your watch model (e.g., `MG-01` will create `MG-01_1.png`, `MG-01_2.png`).
4. **Define the Aesthetic (Palette Configuration):**
  
  * **Base Color:** The primary color of your model's "movement." Enter a hex code (`#1c1c1c`) or **leave it blank to have the engine design a random base color for you.**
  * **Color Harmony:** The underlying principle of your color design. `Analogous` for subtle variations, `Complementary` for a striking two-tone look.
  * **Temperature:** Dial up the creativity. Higher values create more daring and unique color combinations.
  * **Seed:** Input a specific serial number to recreate a known model.
5. **Begin Production:**
  
  * Click **"Generate Art"** and monitor the process in the status bar.

* * *

## 🤝 Contributing

This project is a labor of love. If you have ideas for new "complications" (features), optimizations, or bug fixes, contributions are highly encouraged. Please fork the repository and submit a pull request.

* * *

## 🎇 Future Complications

  * MilleGenesis is an evolving project. Here are some of the advanced "complications" planned for future releases:
  * Trait & Rarity System: Implement a folder-based trait system (case/gold#10.png) to allow for weighted rarities, essential for generative collections like NFTs.
  * Advanced Shaders: Move beyond solid fills with procedural gradients, textures (e.g., carbon fiber, brushed metal), and pattern overlays.
  * Transformational Logic: Introduce subtle, controlled randomness with layer omission, rotation, scaling, and position shifting for more organic and unique outputs.
  * Palette Extraction: A feature to analyze a source image (like a photograph or painting) and automatically extract its dominant colors to use as a base palette.
  * Live Preview & Presets: An instant preview pane that updates as you tweak settings, plus the ability to save and load your favorite configurations.

* * *

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.
