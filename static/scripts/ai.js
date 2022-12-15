const input_image = document.querySelector("#pictures");
const view_image = document.querySelector("#view-image");

const changeImageHandle = (event) => {
    const files = event.target.files[0];
    const reader = new FileReader()
    reader.onload = () => {
        if (reader.readyState === 2) {
            const imageData = {
                data: reader.result
            }

            const formData = new FormData();
            formData.append("image_data", imageData.data);
            
            const Upload = async() => {
                await fetch('/api/image', {
                    method: 'POST',
                    body: formData
                }).then(res => {
                    res.json().then(data => {
                        const image_base64 = "data:image/jpeg;base64," + (data.message);
                        view_image.src = image_base64;
                    })
                })
            }
            Upload()
        }
    }
    reader.readAsDataURL(files)
}

input_image.addEventListener('change', (event) => {
    changeImageHandle(event);
})