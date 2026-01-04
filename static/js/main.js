function toggleSection(sectionId) {
  const content = document.getElementById(sectionId + '-content');
  const icon = document.getElementById(sectionId + '-icon');
  
  if (content.classList.contains('active')) {
    content.style.maxHeight = null;
    content.classList.remove('active');
    icon.textContent = '▼';
    history.pushState(null,null,window.location.pathname);
  } else {
    // Force display temporarily to calculate full height
    content.style.display = 'block';
    content.style.maxHeight = 'none';
    const fullHeight = content.scrollHeight;
    content.style.maxHeight = fullHeight + 'px';
    content.classList.add('active');
    icon.textContent = '▲';
    const parentId = content.parentElement.id;
    if (parentId) {
      history.pushState(null, null, '#' + parentId);
    }
  }
}
document.addEventListener("DOMContentLoaded", function () {
  new Typed(".auto-type", {
    strings: [
      "Made Simple",
      "for Every Citizen"
    ],
    typeSpeed: 80,
    backSpeed: 50,
    backDelay: 1500,
    loop: true
  });
});