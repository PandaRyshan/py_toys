// $(document).ready(function() {
//     $("#submit-btn").click(function() {
//         $(this).html("Processing...").addClass("disabled");
//         $.ajax({
//             url: "/",
//             method: "POST",
//             data: { name: "John", age: 30 },
//             success: function(data) {
//                 // 处理后端返回的数据
//                 $("#submit-btn").html("Commit").removeClass("disabled");
//             },
//             error: function(jqXHR, textStatus, errorThrown) {
//                 // 处理请求失败的情况
//                 $("#submit-btn").html("Commit").removeClass("disabled");
//             }
//         });
//     });
// });

function submitForm() {
    // 将按钮禁用并将文本更改为 Processing...
    document.getElementById("submit-btn").disabled = true;
    document.getElementById("submit-btn").textContent = "Processing...";

    // 使用 fetch 或其他方式提交表单，处理完成后恢复按钮状态
    fetch('/speech/save', {
        method: 'POST',
        body: new FormData(document.getElementById('my-form'))
    }).then(response => {
        // 请求成功，将按钮文本恢复为原文本，启用按钮
        document.getElementById("submit-btn").disabled = false;
        document.getElementById("submit-btn").textContent = "Commit";
    }).catch(error => {
        // 请求失败，将按钮文本恢复为原文本，启用按钮
        document.getElementById("submit-btn").disabled = false;
        document.getElementById("submit-btn").textContent = "Commit";
    });
}