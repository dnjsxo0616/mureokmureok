
  
  function changeContent(contentType) {
    if (contentType === 'board') {
      document.getElementById('content_board').classList.remove('hidden');
      document.getElementById('content_qa').classList.add('hidden');
      document.getElementById('btn_board').classList.add('selected');
      document.getElementById('btn_qa').classList.remove('selected');

    } else if (contentType === 'qa') {
      document.getElementById('content_board').classList.add('hidden');
      document.getElementById('content_qa').classList.remove('hidden');
      document.getElementById('btn_board').classList.remove('selected');
      document.getElementById('btn_qa').classList.add('selected');
    }
  }
  
