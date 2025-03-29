document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("pdf-file");
  const downloadSection = document.getElementById("download-section");
  const downloadLink = document.getElementById("download-link");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // 기본 폼 제출 방지

    const file = fileInput.files[0];
    if (!file) {
      alert("PDF 파일을 선택해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf_file", file);

    try {
      const response = await fetch("/convert", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("변환 중 오류가 발생했습니다.");
      }

      const result = await response.json();

      // 다운로드 링크 업데이트
      downloadLink.href = result.download_url;
      downloadSection.style.display = "block";
    } catch (err) {
      console.error(err);
      alert("파일 업로드 또는 변환에 실패했습니다.");
    }
  });
});
