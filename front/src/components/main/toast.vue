<template>
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <img src="/sd1.png" class="rounded me-2 img-main" alt="...">
                <strong class="me-auto">系统提示</strong>
                <small class="text-body-secondary">{{ time }}</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body text-center">
                {{ message }}
            </div>
        </div>
    </div>
</template>
<script>
export default{
    props: {
        message: {
            type: String,
            required: true
        },
        time: {
            type: String,
            required: true
        }
    }
} 
</script>