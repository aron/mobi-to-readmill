if (window.FormData && document.querySelector) {
  var form = document.querySelector('form');
  var input = form.querySelector('input');
  var fallback = document.getElementById('fallback');

  if (fallback) {
    fallback.parentNode.removeChild(fallback);
  }

  function upload(options) {
    var data = new FormData();
    data.append(options.field || 'file', options.file, options.file.name);

    var xhr = new XMLHttpRequest();
    xhr.open('post', options.url, true);

    xhr.setRequestHeader('X-Requested-With', 'xmlhttprequest')
    xhr.addEventListener('load', function (event) {
      if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
          options.onSuccess();
        } else {
          options.onError();
        }
        options.onComplete();
      }
    }, false);

    xhr.addEventListener('progress', function (event) {
      if (typeof options.onProgress === 'function' && event.lengthComputable) {
        options.onProgress(event.loaded / event.total);
      }
    });

    xhr.send(data);
  }

  function stop(cb) {
    return function (event) {
      event.stopPropagation();
      event.preventDefault();

      if (typeof cb === 'function') {
        return cb(event);
      }
    }
  }

  var dropbox = document.body;
  dropbox.addEventListener('dragenter', stop(function (event) {
    dropbox.classList.add('active');
  }), false);

  dropbox.addEventListener('dragleave', function (event) {
    dropbox.classList.remove('active');
  }, false);

  dropbox.addEventListener('dragover', stop(), false);

  dropbox.addEventListener("drop", stop(function (event) {
    dropbox.classList.add('loading');
    dropbox.classList.remove('active');
    upload({
      url: form.action,
      file: event.dataTransfer.files[0],
      field: input.name,
      onSuccess: function () {
        alert('whoop!');
      },
      onComplete: function () {
        dropbox.classList.remove('loading');
      },
      onError: function () {
        alert('boo!');
      },
      onProgress: function (progress) {
        console.log(progress * 100);
      }
    });
  }), false);
}
