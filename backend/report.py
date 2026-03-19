def generate_report(metadata, video_forensics=None, image_forensics=None, audio_forensics=None, filename=""):
    
    model = str(metadata.get('Model', metadata.get('DeviceModelName', ''))).strip()
    make = str(metadata.get('Make', metadata.get('Manufacturer', ''))).strip()
    has_hard_metadata = any([model, make]) and model.lower() != "unknown" and make.lower() != "unknown"
    device_name = f"{make} {model}".strip() or "Unknown"
    
    status = "Unknown"
    summary = "Pending analysis."
    fake_prob = 0

    if audio_forensics:
        status_label = audio_forensics.get("label", "Authentic")
        details = audio_forensics.get("details", "Unknown")
        fake_prob = audio_forensics.get("overall_score", 0)
        real_conf = audio_forensics.get("real_confidence", 100 - fake_prob)
        
        if status_label == "Manipulated":
            status = "Manipulated"
            summary = f"Audio Forgery Detected: Identified as {details} with {round(fake_prob, 2)}% confidence."
        elif status_label == "Suspicious":
            status = "Suspicious"
            summary = f"Suspicious Audio: {details}. Manipulation probability at {round(fake_prob, 2)}%."
        else:
            status = "Authentic"
            summary = f"Verified Original Audio: Passed integrity check. Audio is {round(real_conf, 2)}% Authentic."

    elif video_forensics:
        fake_prob = (video_forensics['dfdc']['deepfake_score'] * 0.6) + (video_forensics['faceforensics']['ff_score'] * 0.4)

        if not has_hard_metadata:
            if fake_prob > 45:
                status = "Manipulated"
                summary = f"Video Forgery Detected: High AI manipulation score ({round(fake_prob, 2)}%) and missing camera metadata."
            elif 30 <= fake_prob <= 45:
                status = "Suspicious"
                summary = f"Suspicious Video: No device metadata found. Frame texture matches AI generation patterns."
            else:
                status = "Authentic"
                summary = "Real Video: Metadata stripped, but frame-by-frame pixel analysis is consistent."
        else:
            status = "Authentic" if fake_prob < 60 else "Manipulated"
            summary = f"Verified Original Video: Captured via {device_name}." if fake_prob < 60 else "Hardware found, but AI facial/frame edits detected."

    elif image_forensics:
        fake_prob = image_forensics.get("cnn_score", 0)
        is_pdf = image_forensics.get("is_pdf", False)
        
        media_type = "Document" if is_pdf else "Image"

        if not has_hard_metadata:
            if fake_prob > 45:
                status = "Manipulated"
                summary = f"{media_type} Forgery Detected: High manipulation probability ({round(fake_prob, 2)}%) and missing metadata."
            elif 30 <= fake_prob <= 45:
                status = "Suspicious"
                summary = f"Suspicious {media_type}: No metadata found. Pixel analysis indicates possible AI generation or tampering."
            else:
                status = "Authentic"
                summary = f"Verified {media_type}: Metadata stripped, but pixel analysis is consistent with original capture."
        else:
            status = "Authentic" if fake_prob < 60 else "Manipulated"
            summary = f"Verified Original {media_type}: Captured via {device_name}." if fake_prob < 60 else f"Hardware found, but AI edits detected in {media_type.lower()}."

    return {
        "authenticity_status": status,
        "forensic_summary": summary,
        "manipulation_probability": round(fake_prob, 2),
        "metadata_integrity": "Preserved" if has_hard_metadata else "Compromised/Missing",
        "source_hardware": device_name
    }