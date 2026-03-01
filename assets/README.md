# Kenkoumon Assets

Shared assets for the Kenkoumon application.

## Structure

```
assets/
├── images/
│   ├── mascot.png          # Kenkoumon mascot character
│   └── ...
└── README.md
```

## Usage

### Backend (FastAPI)

Access via `/static/images/mascot.png`:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

### iOS App

Reference in SwiftUI:

```swift
Image("Mascot")
    .resizable()
    .scaledToFit()
```

### Documentation

Use in markdown:

```markdown
![Kenkoumon Mascot](docs/assets/images/mascot.png)
```

## Mascot

The Kenkoumon mascot represents a friendly health companion character.

- **File:** `mascot.png`
- **Size:** ~810 KB
- **Format:** PNG with transparency
