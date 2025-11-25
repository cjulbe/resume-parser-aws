const form = document.getElementById("uploadForm");
const responseBox = document.getElementById("response");
const API_BASE_URL = "__API_URL__";

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("resumeFile");
    const file = fileInput.files[0];
    if (!file) return;
    
    // --- Basic file validation (requirement #3) ---
    const allowedExtensions = [".pdf", ".docx"];
    const fileName = file.name.toLowerCase();

    if (!allowedExtensions.some(ext => fileName.endsWith(ext))) {
        responseBox.textContent = "Error: Only PDF or DOCX files are allowed.";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    responseBox.textContent = "Uploading...";

    try {
        const res = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        // Check if backend returned HTML or a 500 and stop here
        if (!res.ok) {
            const text = await res.text();
            throw new Error(`Server error ${res.status}:\n${text}`);
        }

        const data = await res.json();
        responseBox.textContent = JSON.stringify(data, null, 2);
        
    } catch (err) {
        responseBox.textContent = "Error: " + err.message;
    }
});
