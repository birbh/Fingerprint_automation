# Suspect Images Directory

This directory is used to store suspect photos.

## Usage

When enrolling a fingerprint, you can provide the path to a suspect's photo.
The photo will be automatically displayed when a fingerprint match is found.

## Recommendations

- **Format**: JPEG, PNG, or other common image formats
- **Size**: Keep images under 5MB for fast loading
- **Resolution**: 800x600 or higher recommended
- **Naming**: Use descriptive names like `suspect_001.jpg`, `john_doe.jpg`, etc.

## Example

```
suspect_images/
├── suspect_001.jpg
├── suspect_002.jpg
├── john_doe.png
└── jane_smith.jpg
```

When enrolling:
```
Image path (optional): suspect_images/suspect_001.jpg
```

Or use absolute paths:
```
Image path (optional): /home/user/photos/suspect.jpg
```

## Security Note

Store sensitive images securely:
- Use appropriate file permissions
- Consider encryption for sensitive data
- Backup regularly
