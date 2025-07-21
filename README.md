# 🖌️ Virtual Painter with Hand Gestures

This project is a real-time virtual painter using **OpenCV**, **MediaPipe**, and **Python**. You can draw on the screen using **hand gestures** detected from your webcam.

---

## ✨ Features

- 🎨 **Draw on a virtual canvas** using only your **index finger**
- 🎨 **Color palette** selection using hand movement to the top of the screen
- 🌈 **Rainbow brush** when showing **3 fingers**
- ❌ **Erase** using a **closed fist**
- 💥 **Clear canvas with explosion animation** by raising **5 fingers**
- 💾 **Auto-save drawings** with **4 fingers**
- 🖐️ **Real-time hand tracking** using MediaPipe

---

## 📦 Requirements

Install the required dependencies using pip:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ How to Run

Make sure your webcam is connected, then run:

```bash
python paint.py
```

Press **`q`** to quit the application.

---

## 🧠 Controls & Gestures

| Gesture             | Action                           |
|---------------------|----------------------------------|
| 1 finger (Index)    | Draw                             |
| 3 fingers           | Rainbow color drawing            |
| 0 fingers (Fist)    | Eraser                           |
| 4 fingers           | Save canvas as PNG               |
| 5 fingers           | Clear canvas with explosion      |
| Finger near top bar | Change brush color               |

---

## 🎨 Color Palette

The top bar of the screen displays selectable colors:

- 🔴 Red
- 🟢 Green
- 🔵 Blue
- 🟡 Yellow
- ⚪ White
- ⚫ Black (Eraser)

---

## 📸 Example Output

![demo-preview](demo.gif)  
*Live drawing with color change and hand detection.*

---

## 🛠️ Built With

- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)

---

## 🧑‍💻 Author

**Your Name**  
Feel free to customize this with your name, GitHub profile, or contact info.

---

## 📄 License

This project is open-source and free to use under the MIT License.
