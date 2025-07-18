# 🛰️ ISS Real-Time Dashboard

A real-time dashboard for tracking the International Space Station (ISS) position and crew information.

## Features

- **Live ISS Position**: Real-time latitude and longitude tracking
- **Interactive Map**: Visual representation of ISS location on a world map
- **Current Crew**: Display of astronauts currently aboard the ISS
- **Auto-refresh**: Optional automatic data updates every 10 seconds
- **Manual Refresh**: Button to manually update all data

## Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework
- **Folium** - Interactive maps
- **Open Notify API** - ISS position and astronaut data
- **Pandas** - Data manipulation

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/iss-dashboard.git
cd iss-dashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
streamlit run iss_dashboard.py
```

## Usage

1. Open your web browser and go to `http://localhost:8501`
2. View the real-time ISS position on the map
3. Check the current crew information
4. Use the refresh button or enable auto-refresh for live updates

## API Sources

- [Open Notify ISS Location API](http://api.open-notify.org/iss-now.json)
- [Open Notify Astronauts API](http://api.open-notify.org/astros.json)

## Project Structure

```
iss-dashboard/
├── iss_dashboard.py          # Main dashboard application
├── ISS_PYTHON_TRACKING_ISL.ipynb # Jupyter notebook with analysis
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Screenshots

![ISS Dashboard](https://via.placeholder.com/800x400?text=ISS+Dashboard+Screenshot)

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Soumitra Kumar**
- GitHub: [@yourusername](https://github.com/yourusername)

---

*Made with ❤️ by Soumitra Kumar*