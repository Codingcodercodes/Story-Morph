document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const button = form.querySelector('button');

  form.addEventListener('submit', () => {
    button.disabled = true;
    button.textContent = 'Generating...';
  });
});

window.addEventListener('DOMContentLoaded', () => {
  const genreSelect = document.querySelector('select[name="genre"]');
  const submitButton = document.querySelector('button[type="submit"]');

  function applyTheme(genre) {
    const body = document.body;
    body.className = "";  // Reset all classes
    submitButton.className = ""; // Reset button class

    switch (genre) {
      case 'fantasy':
        body.classList.add('fantasy-theme');
        submitButton.classList.add('fantasy-btn');
        break;
      case 'sci-fi':
        body.classList.add('sci-fi-theme');
        submitButton.classList.add('sci-fi-btn');
        break;
      case 'rom-com':
        body.classList.add('rom-com-theme');
        submitButton.classList.add('rom-com-btn');
        break;
      case 'thriller':
        body.classList.add('thriller-theme');
        submitButton.classList.add('thriller-btn');
        break;
      case 'mystery':
        body.classList.add('mystery-theme');
        submitButton.classList.add('mystery-btn');
        break;
      case 'horror':
        body.classList.add('horror-theme');
        submitButton.classList.add('horror-btn');
        break;
    }
  }

  // Initial call
  applyTheme(genreSelect.value);

  // Change on genre change
  genreSelect.addEventListener('change', (e) => {
    applyTheme(e.target.value);
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const themeToggle = document.getElementById('themeToggle');
  const body = document.body;

  const savedTheme = localStorage.getItem('storyTheme');
  if (savedTheme === 'dark') {
    body.classList.add('dark-theme');
    themeToggle.checked = true;
  }

  if (themeToggle) {
    themeToggle.addEventListener('change', () => {
      if (themeToggle.checked) {
        body.classList.add('dark-theme');
        localStorage.setItem('storyTheme', 'dark');
      } else {
        body.classList.remove('dark-theme');
        localStorage.setItem('storyTheme', 'light');
      }
    });
  }
});

