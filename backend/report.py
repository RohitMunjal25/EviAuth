def generate_report(metadata, video_forensics=None, image_forensics=None, audio_forensics=None, filename=""):
    model = str(metadata.get('Model', metadata.get('DeviceModelName', ''))).strip()
    make = str(metadata.get('Make', metadata.get('Manufacturer', ''))).strip()
    has_hard_metadata = any([model, make]) and model.lower() != "unknown" and make.lower() != "unknown"
    device_name = f"{make} {model}".strip() if has_hard_metadata else "Unknown"
    
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
            summary = f"Audio Forgery Detected: Identified as {details} ({round(fake_prob, 2)}%)."
        elif status_label == "Suspicious" or fake_prob > 50:
            status = "Suspicious"
            summary = f"Highly Compressed Audio. Manipulation probability: {round(fake_prob, 2)}%."
        else:
            status = "Authentic"
            summary = f"Verified Original Audio: Passed integrity check ({round(real_conf, 2)}% Authentic)."

    elif video_forensics:
        dfdc_score = video_forensics.get('dfdc', {}).get('deepfake_score', 0)
        ff_score = video_forensics.get('faceforensics', {}).get('ff_score', 0)
        
        fake_prob = (dfdc_score * 0.7) + (ff_score * 0.3)

        if fake_prob > 65: 
            status = "Manipulated"
            summary = f"Video Forgery Detected: High AI artifact patterns found ({round(fake_prob, 2)}%)."
        elif 45 <= fake_prob <= 65: 
            status = "Suspicious"
            summary = "Potential Manipulation: High noise or compression artifacts detected."
        else: 
            status = "Authentic"
            summary = "Verified Original: Video pixels and neural flow are consistent."

        if has_hard_metadata and fake_prob < 55:
            status = "Authentic"
            summary = f"Verified Original: Securely captured via {device_name}."

    elif image_forensics:
        tampering_score = image_forensics.get("cnn_score", 0) 
        genai_score = image_forensics.get("genai_score", 0)   
        is_pdf = image_forensics.get("is_pdf", False)
        
        if is_pdf:
            fake_prob = tampering_score
            if fake_prob > 75:
                status = "Manipulated"
                summary = f"Document Forgery Detected: Heavy digital overlays found ({round(fake_prob, 2)}%)."
            elif 50 < fake_prob <= 75:
                status = "Suspicious"
                summary = f"Suspicious PDF: Conversion artifacts detected ({round(fake_prob, 2)}%)."
            else:
                status = "Authentic"
                summary = "Document Verified: No severe digital tampering detected."
        else:
            if has_hard_metadata:
                if genai_score > 80:
                    status = "AI Generated (Spoofed Metadata)"
                    summary = f"Warning: Device says {device_name}, but high AI patterns found."
                    fake_prob = genai_score
                else:
                    fake_prob = tampering_score
                    if tampering_score < 50:
                        status = "Authentic"
                        summary = f"Verified Original: Clean capture via {device_name}."
                    else:
                        status = "Manipulated"
                        summary = f"Hardware found ({device_name}), but editing detected ({round(tampering_score, 2)}%)."
            else:
                if genai_score > 80 and tampering_score < 40:
                    status = "Suspicious"
                    summary = f"Image degraded. High synthetic patterns ({round(genai_score, 2)}%)."
                    fake_prob = max(tampering_score, 50.0) 
                elif genai_score > 60 and tampering_score >= 40:
                    status = "AI Generated"
                    summary = f"Synthetic Image: Matches Generative AI patterns ({round(genai_score, 2)}%)."
                    fake_prob = genai_score
                elif tampering_score > 50:
                    status = "Manipulated"
                    summary = f"Forgery Detected: Digital editing found ({round(tampering_score, 2)}%)."
                    fake_prob = tampering_score
                else:
                    status = "Authentic"
                    summary = "Real Image: Pixels are natural despite missing metadata."
                    fake_prob = max(tampering_score, genai_score)

    return {
        "authenticity_status": status,
        "forensic_summary": summary,
        "manipulation_probability": round(fake_prob, 2),
        "metadata_integrity": "Preserved" if has_hard_metadata else "Compromised/Missing",
        "source_hardware": device_name
    }