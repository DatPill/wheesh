function copyLink(link, button) {
    const tempInput = document.createElement('input');
    tempInput.value = link;
    document.body.appendChild(tempInput);
    tempInput.select();
    tempInput.setSelectionRange(0, 99999);
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    button.setAttribute('data-bs-toggle', 'tooltip');
    button.setAttribute('data-bs-placement', 'top');
    button.setAttribute('title', 'Скопировано!');

    const tooltip = new bootstrap.Tooltip(button, {trigger: 'manual'});
    tooltip.show();

    setTimeout(() => {
        tooltip.hide();
        tooltip.dispose();
        button.removeAttribute('data-bs-toggle');
        button.removeAttribute('data-bs-placement');
        button.removeAttribute('title');
    }, 2000);
  }
