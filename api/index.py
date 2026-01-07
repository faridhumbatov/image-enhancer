// HTML-dəki elementləri seçirik
const generateBtn = document.getElementById('generateBtn'); // "Yarat" düyməsinin ID-si
const promptInput = document.getElementById('promptInput'); // Mətn yazılan yerin ID-si
const imageElement = document.getElementById('resultImage'); // Şəklin göstəriləcəyi <img>
const loadingSpinner = document.getElementById('loading'); // Yüklənmə ikonu (varsa)

// Hugging Face API Tokeniniz (Bura öz tokeninizi yapışdırın)
const TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"; 

async function generateImage() {
    const prompt = promptInput.value;
    
    if (prompt === "") {
        alert("Zəhmət olmasa təsviri daxil edin!");
        return;
    }

    // Yüklənir mesajı və ya animasiyası (varsa aktivləşdirin)
    if(loadingSpinner) loadingSpinner.style.display = 'block';
    generateBtn.disabled = true;
    generateBtn.innerText = "Yaradılır...";

    try {
        // Hugging Face-ə sorğu göndəririk (Stable Diffusion XL modeli)
        const response = await fetch(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${TOKEN}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ inputs: prompt }),
            }
        );

        if (!response.ok) {
            throw new Error("Xəta baş verdi! Tokeni yoxlayın və ya bir az gözləyin.");
        }

        // Gələn cavabı (Blob) şəkilə çeviririk
        const blob = await response.blob();
        const imgUrl = URL.createObjectURL(blob);
        
        // Şəkli ekranda göstəririk
        imageElement.src = imgUrl;

    } catch (error) {
        console.error(error);
        alert("Şəkil yaradılarkən xəta oldu: " + error.message);
    } finally {
        // Düyməni əvvəlki halına qaytarırıq
        if(loadingSpinner) loadingSpinner.style.display = 'none';
        generateBtn.disabled = false;
        generateBtn.innerText = "Yarat 🚀";
    }
}

// Düyməyə klik hadisəsini əlavə edirik
generateBtn.addEventListener('click', generateImage);
