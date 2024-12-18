function handleTapBehavior() {
  // Only on screens that are smaller than Bootstrap's lg
  // fixme: DOESNT WORK WITH ALBUM IPADS
  const isSmallScreen = window.innerWidth < 992;

  const reservedElements = document.querySelectorAll('.reserved-present');

  if (isSmallScreen) {
    reservedElements.forEach((element) => {
      element.addEventListener('click', toggleTappedClass);
    });
  } else {
    reservedElements.forEach((element) => {
      element.removeEventListener('click', toggleTappedClass);
      element.classList.remove('tapped'); // Remove `tapped` state
    });
  }
}

function toggleTappedClass(e) {
  e.preventDefault();
  const isTapped = this.classList.contains('tapped');

  document.querySelectorAll('.reserved-present').forEach(el => el.classList.remove('tapped'));

  if (!isTapped) {
    this.classList.add('tapped');
  }
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('.reserved-present')) {
    document.querySelectorAll('.reserved-present').forEach(el => el.classList.remove('tapped'));
  }
});

handleTapBehavior();

// Recheck on resize
window.addEventListener('resize', handleTapBehavior);
