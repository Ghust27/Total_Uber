document.getElementById('fetchCookies').addEventListener('click', async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab && tab.url) {
      if (chrome.cookies && chrome.cookies.getAll) {
        chrome.cookies.getAll({ url: tab.url }, (cookies) => {
          let sid = '';
          let csid = '';

          for (let cookie of cookies) {
            if (cookie.name === 'sid') {
              sid = cookie.value;
            }
            if (cookie.name === 'csid') {
              csid = cookie.value;
            }
          }

          const cookieOutput = sid && csid ? `sid=${sid};csid=${csid}` : '';
          document.getElementById('cookieOutput').value = cookieOutput;

          const message = document.getElementById('message');
          const copyButton = document.getElementById('copyCookies');
          if (cookieOutput) {
            message.textContent = '';
            copyButton.disabled = false;
          } else {
            message.textContent = 'Não foi possível encontrar os cookies.';
            message.classList.add('error');
            copyButton.disabled = true;
            setTimeout(() => {
              message.classList.remove('error');
              message.textContent = '';
            }, 4000);
          }
        });
      } else {
        throw new Error('API chrome.cookies.getAll não disponível');
      }
    } else {
      throw new Error('Tab URL not found');
    }
  } catch (error) {
    console.error('Erro ao obter os cookies:', error);
    const message = document.getElementById('message');
    message.textContent = 'Erro ao obter os cookies.';
    message.classList.add('error');
    setTimeout(() => {
      message.classList.remove('error');
      message.textContent = '';
    }, 4000);
  }
});

document.getElementById('copyCookies').addEventListener('click', () => {
  const cookieOutput = document.getElementById('cookieOutput').value;
  if (cookieOutput) {
    navigator.clipboard.writeText(cookieOutput).then(() => {
      const message = document.getElementById('message');
      message.textContent = 'Cookies copiados para a área de transferência!';
      message.classList.add('visible');
      setTimeout(() => {
        message.classList.remove('visible');
        message.textContent = '';
      }, 4000);
    });
  }
});
