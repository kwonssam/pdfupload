document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("pdf-file");
  const resultSection = document.getElementById("result-section");
  const previewImage = document.getElementById("preview-image");
  const downloadLink = document.getElementById("download-link");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // 페이지 새로고침 방지

    const file = fileInput.files[0];
    if (!file) {
      alert("PDF 파일을 선택해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf_file", file);

    try {
      // Flask 서버의 /convert 엔드포인트로 파일 업로드
      const response = await fetch("/convert", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("서버 응답 오류");
      }

      const result = await response.json();

      // 서버로부터 받은 다운로드 URL
      const imageUrl = result.download_url;

      // 이미지 미리보기 및 다운로드 링크 설정
      previewImage.src = imageUrl;
      downloadLink.href = imageUrl;

      // 결과 섹션 표시
      resultSection.style.display = "block";
    } catch (err) {
      console.error("에러 발생:", err);
      alert("변환 중 문제가 발생했습니다. 다시 시도해주세요.");
    }
  });
});
