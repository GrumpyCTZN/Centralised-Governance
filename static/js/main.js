function toggleSection(sectionId) {
  const content = document.getElementById(sectionId + '-content');
  const icon = document.getElementById(sectionId + '-icon');
  
  if (content.style.maxHeight) {
    content.style.maxHeight = null;
    content.classList.remove('active');
    icon.textContent = '▼';
  } else {
    content.style.maxHeight = content.scrollHeight + 'px';
    content.classList.add('active');
    icon.textContent = '▲';
  }
}