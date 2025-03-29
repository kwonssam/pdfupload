document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("pdf-file");
  const resultSection = document.getElementById("result-section");
  const previewImage = document.getElementById("preview-image");
  const downloadLink = document.getElementById("download-link");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // 새로고침 방지

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
        throw new Error("서버 오류 또는 변환 실패");
      }

      const result = await response.json();

      if (result.error) {
        alert("에러: " + result.error);
        return;
      }

      // 변환된 PNG 이미지 URL
      const imageUrl = result.download_url;

      // 이미지 미리보기 및 다운로드 링크 설정
      previewImage.src = imageUrl;
      downloadLink.href = imageUrl;

      resultSection.style.display = "block"; // 결과 섹션 표시
    } catch (err) {
      console.error("에러 발생:", err);
      alert("변환 중 문제가 발생했습니다.");
    }
  });
});
