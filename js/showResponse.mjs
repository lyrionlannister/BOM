export function showResponse(data, status) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@10';
    document.head.appendChild(script);
    script.onload = () => {
        Swal.fire({
            title: data.message,
            icon: status === 200 ? 'success' : 'error',
            timer: 3000,
            timerProgressBar: true,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            customClass: {
                popup: 'my-swal-popup', 
                content: 'my-swal-content'
            },
        });
    };   
}