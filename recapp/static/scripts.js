document.addEventListener('DOMContentLoaded', function() {
    let selectedProducts = {
      dataset1: null,
      dataset2: null,
      dataset3: null
    };
    const notificationIcon = document.querySelector('.notification-icon');
    const notificationCount = document.querySelector('.notification-count');
    function updateNotificationCount() {
      const currentCount = parseInt(notificationCount.innerText);
      notificationCount.innerText = currentCount + 1;
      notificationCount.style.display = 'inline'; // Afficher le compteur lorsque non nul
  }
  
    document.getElementById('datasetSelection').addEventListener('change', function() {
      const selectedDataset = this.value;
      hideAllSearchForms();
      if (selectedDataset === '2') {
        document.getElementById('dataset2Search').style.display = 'block';
        resetDataset2SearchResults();
      } else if (selectedDataset === '3') {
        document.getElementById('dataset3Search').style.display = 'block';
        resetDataset3SearchResults();
      }
    });
    function resetDataset3SearchResults() {
      const resultsContainer = document.getElementById('results3');
      resultsContainer.innerHTML = '';    
      const pagesContainer = document.getElementById('pagesWrapper3');
      pagesContainer.innerHTML = '';    
      // Hide the "Confirmer" button for dataset3
      const searchButton = document.querySelector('#pagesWrapper3 button');
      if (searchButton) {
        searchButton.style.display = 'none';
      }
    }
    function resetDataset2SearchResults() {
      const resultsContainer = document.getElementById('results2');
      resultsContainer.innerHTML = '';    
      const pagesContainer = document.getElementById('pagesWrapper2');
      pagesContainer.innerHTML = '';    
      // Hide the "Confirmer" button for dataset2
      const searchButton = document.querySelector('#pagesWrapper2 button');
      if (searchButton) {
        searchButton.style.display = 'none';
      }
    }        
    function hideAllSearchForms() {
      document.getElementById('dataset2Search').style.display = 'none';
      document.getElementById('dataset3Search').style.display = 'none';
    }
  
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', event => {
        event.preventDefault();
  
        const datasetNumber = form.dataset_number.value;
        const keyword = form.keyword.value;
  
        // Reset selected product for the current dataset
        selectedProducts[`dataset${datasetNumber}`] = null;
  
        fetchResults(datasetNumber, keyword, 1);
      });
    });
    notificationIcon.addEventListener('click', function() {
      // Récupérer le nombre actuel de notifications
      const currentCount = parseInt(notificationCount.innerText);

      if (currentCount > 0) {
          // Afficher le message de succès avec le nombre de produits ajoutés
          Swal.fire({
              icon: 'success',
              title: 'Produits ajoutés avec succès !',
              text: `Vous avez ajouté ${currentCount} produit(s) à votre liste.`
          });

          // Réinitialiser le compteur de notifications
          notificationCount.innerText = '0';
          notificationCount.style.display = 'none'; // Cacher le compteur
      } else {
          // Afficher un message si aucune notification n'est présente
          Swal.fire({
              icon: 'info',
              title: 'Aucun produit ajouté',
              text: 'Vous n\'avez ajouté aucun produit à votre liste.'
          });
      }
    });

  
    function fetchResults(datasetNumber, keyword, page) {
      fetch(`/recommend/?keyword=${keyword}&dataset_number=${datasetNumber}&page=${page}`)
        .then(response => response.json())
        .then(data => {
          const resultsContainer = document.getElementById(`results${datasetNumber}`);
          resultsContainer.innerHTML = '';
  
          for (let i = 0; i < data.results.length; i += 3) {
            const row = document.createElement('div');
            row.className = 'product-row row';
  
            const product1 = document.createElement('div');
            product1.className = 'product col';
  
            // Create the checkbox for product 1
            const checkbox1 = createProductCheckbox(data.results[i].id, datasetNumber);
            product1.appendChild(checkbox1);
  
            // Ajout du reste du contenu pour le produit 1
            const product1Content = document.createElement('div');
            product1Content.innerHTML = `<h2>${data.results[i].name}</h2>
            <p>${data.results[i].description || ''}</p>
            ${datasetNumber == 1 ? `<p> ${data.results[i].price || ''}</p>` : ''}
            ${datasetNumber == 2 ? `<p>Prix: ${data.results[i].price || ''}</p><p>Marque: ${data.results[i].brand || ''}</p>` : ''}
            ${datasetNumber == 3 ? `<p>Prix: ${data.results[i].price || ''}</p>` : ''}`;
            product1.appendChild(product1Content);

            if (datasetNumber === '1') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                        item.libelle_article === data.results[i].name &&
                        item.similar_product_in_carrefour &&
                        item.similar_product_in_founa
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product1.appendChild(marker);
                    }
                  });
              }
  
            if (datasetNumber === '2') {
              fetch('/get_dataset1_data/')
                .then(response => response.json())
                .then(dataset1Data => {
                  // Compare the product with the "Dataset1" data
                  const matchingDataset1Item = dataset1Data.results.find(item =>
                    item.similar_product_in_carrefour === data.results[i].name &&
                    item.prix_produit_carrefour === data.results[i].price &&
                    item.description_produit_carrefour === data.results[i].description
                  );
  
                  if (matchingDataset1Item) {
                    const marker = document.createElement('div');
                    marker.className = 'checked-marker';
                    product1.appendChild(marker);
                  }
                });
            }

            if (datasetNumber === '3') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const matchingDataset1Item = dataset1Data.results.find(item =>
                      item.similar_product_in_dataset3 === data.results[i].name &&
                      item.prix_produit_dataset3 === data.results[i].price &&
                      item.description_produit_dataset3 === data.results[i].description
                    );
    
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product1.appendChild(marker);
                    }
                  });
              }
  
            row.appendChild(product1);
  
            if (data.results[i + 1]) {
              const product2 = document.createElement('div');
              product2.className = 'product col';
  
              // Create the checkbox for product 2
              const checkbox2 = createProductCheckbox(data.results[i + 1].id, datasetNumber);
              product2.appendChild(checkbox2);
  
              // Ajout du reste du contenu pour le produit 2
              const product2Content = document.createElement('div');
              product2Content.innerHTML = `<h2>${data.results[i + 1].name} </h2>
              <p>${data.results[i + 1].description || ''}</p>
              ${datasetNumber == 1 ? `<p> ${data.results[i + 1].price || ''}</p>` : ''}
              ${datasetNumber == 2 ? `<p>Prix: ${data.results[i + 1].price || ''}</p><p>Marque: ${data.results[i + 1].brand || ''}</p>` : ''}
              ${datasetNumber == 3 ? `<p>Prix: ${data.results[i + 1].price || ''}</p>` : ''}`;
              product2.appendChild(product2Content);

              if (datasetNumber === '1') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                        item.libelle_article === data.results[i + 1].name &&
                        item.similar_product_in_carrefour &&
                        item.similar_product_in_founa
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product2.appendChild(marker);
                    }
                  });
              }
  
              if (datasetNumber === '2') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                      item.similar_product_in_carrefour === data.results[i + 1].name &&
                      item.prix_produit_carrefour === data.results[i + 1].price &&
                      item.description_produit_carrefour === data.results[i + 1].description
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product2.appendChild(marker);
                    }
                  });
              }
              if (datasetNumber === '3') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                      item.similar_product_in_dataset3 === data.results[i + 1].name &&
                      item.prix_produit_dataset3 === data.results[i + 1].price &&
                      item.description_produit_dataset3 === data.results[i + 1].description
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product2.appendChild(marker);
                    }
                  });
              }
  
              row.appendChild(product2);
            }
            if (data.results[i + 2]) {
              const product3 = document.createElement('div');
              product3.className = 'product col';
  
              // Create the checkbox for product 2
              const checkbox3 = createProductCheckbox(data.results[i + 2].id, datasetNumber);
              product3.appendChild(checkbox3);
  
              // Ajout du reste du contenu pour le produit 2
              const product3Content = document.createElement('div');
              product3Content.innerHTML = `<h2>${data.results[i + 2].name} </h2>
              <p>${data.results[i + 2].description || ''}</p>
              ${datasetNumber == 1 ? `<p> ${data.results[i + 2].price || ''}</p>` : ''}
              ${datasetNumber == 2 ? `<p>Prix: ${data.results[i + 2].price || ''}</p><p>Marque: ${data.results[i + 2].brand || ''}</p>` : ''}
              ${datasetNumber == 3 ? `<p>Prix: ${data.results[i + 2].price || ''}</p>` : ''}`;
              product3.appendChild(product3Content);

              if (datasetNumber === '1') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                        item.libelle_article === data.results[i + 2].name &&
                        item.similar_product_in_carrefour &&
                        item.similar_product_in_founa
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product3.appendChild(marker);
                    }
                  });
              }
  
              if (datasetNumber === '2') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                      item.similar_product_in_carrefour === data.results[i + 2].name &&
                      item.prix_produit_carrefour === data.results[i + 2].price &&
                      item.description_produit_carrefour === data.results[i + 2].description
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product3.appendChild(marker);
                    }
                  });
              }
              if (datasetNumber === '3') {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    // Compare the product with the "Dataset1" data
                    const dataset1Items = dataset1Data.results;
                    const matchingDataset1Item = dataset1Items.find(item =>
                      item.similar_product_in_dataset3 === data.results[i + 2].name &&
                      item.prix_produit_dataset3 === data.results[i + 2].price &&
                      item.description_produit_dataset3 === data.results[i + 2].description
                    );
  
                    if (matchingDataset1Item) {
                      const marker = document.createElement('div');
                      marker.className = 'checked-marker';
                      product3.appendChild(marker);
                    }
                  });
              }
  
              row.appendChild(product3);
            }
            resultsContainer.appendChild(row);
          }
  
          const pagesContainer = document.getElementById(`pagesWrapper${datasetNumber}`);
          pagesContainer.innerHTML = '';
          pagesContainer.className = 'pages';
  
          if (page > 1) {
            const previousPageItem = document.createElement('li');
            previousPageItem.className = 'page-item';
            const previousPageLink = document.createElement('a');
            previousPageLink.href = '#';
            previousPageLink.innerText = '<';
            previousPageLink.addEventListener('click', event => {
              event.preventDefault();
              fetchResults(datasetNumber, keyword, page - 1);
            });
            previousPageItem.appendChild(previousPageLink);
            pagesContainer.appendChild(previousPageItem);
          }
  
          for (let i = Math.max(1, page - 2); i <= Math.min(data.total_pages, page + 2); i++) {
            const pageItem = document.createElement('li');
            pageItem.className = 'page-item';
            if (i === page) {
              pageItem.classList.add('active');
              pageItem.innerHTML = `<strong>${i}</strong>`;
            } else {
              const pageLink = document.createElement('a');
              pageLink.href = '#';
              pageLink.innerText = i;
              pageLink.addEventListener('click', event => {
                event.preventDefault();
                fetchResults(datasetNumber, keyword, i);
              });
              pageItem.appendChild(pageLink);
            }
            pagesContainer.appendChild(pageItem);
          }
  
          if (page < data.total_pages) {
            const nextPageItem = document.createElement('li');
            nextPageItem.className = 'page-item';
            const nextPageLink = document.createElement('a');
            nextPageLink.href = '#';
            nextPageLink.innerText = '>';
            nextPageLink.addEventListener('click', event => {
              event.preventDefault();
              fetchResults(datasetNumber, keyword, page + 1);
            });
            nextPageItem.appendChild(nextPageLink);
            pagesContainer.appendChild(nextPageItem);
          }
  
          // Ajout du bouton de recherche dataset2
          if (datasetNumber === '2') {
            const searchButton = document.createElement('button');
            searchButton.innerText = 'Confirmer';
            searchButton.className = 'btn btn-primary';
            searchButton.addEventListener('click', () => {
              const selectedProduct1 = selectedProducts.dataset1;
              const selectedProduct2 = selectedProducts.dataset2;
              if (selectedProduct1 && selectedProduct2) {
                fetch('/get_dataset1_data/')
                  .then(response => response.json())
                  .then(dataset1Data => {
                    const matchingDataset1Item = dataset1Data.results.find(item =>
                      item.similar_product_in_carrefour === data.results.find(result => result.id === selectedProduct2).name &&
                      item.prix_produit_carrefour === data.results.find(result => result.id === selectedProduct2).price &&
                      item.description_produit_carrefour === data.results.find(result => result.id === selectedProduct2).description
                    );
                    if (matchingDataset1Item) {
                      const message = 'Le produit sélectionné dans Carrefour est déjà associé à un produit dans Monoprix. Voulez-vous annuler la sélection ?';
                      Swal.fire({
                        title: 'Confirmation',
                        text: message,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Continuer',
                        cancelButtonText: 'Annuler'
                      }).then((result) => {
                        if (result.value) {
                          // L'utilisateur a cliqué sur "Continuer"
                          // Effectuez les actions nécessaires ici
                          const dataset1_id = selectedProduct1;
                          const dataset2_info = {
                            name: data.results.find(result => result.id === selectedProduct2).name,
                            price: data.results.find(result => result.id === selectedProduct2).price,
                            description: data.results.find(result => result.id === selectedProduct2).description
                          };
                          sendDataToServer(dataset1_id, dataset2_info, null, datasetNumber); // Passer le numéro de dataset
                          updateNotificationCount();
                          showSuccessAlert();
                          updateSelectedProducts(datasetNumber, selectedProducts[`dataset${datasetNumber}`]);
                          resetSelectedProduct(datasetNumber);
                        } else {
                          // L'utilisateur a cliqué sur "Annuler"
                          // Réinitialisez la sélection du produit
                          resetSelectedProduct(datasetNumber);
                        }
                      });
                    } else {
                      const dataset1_id = selectedProduct1;
                      const dataset2_info = {
                        name: data.results.find(result => result.id === selectedProduct2).name,
                        price: data.results.find(result => result.id === selectedProduct2).price,
                        description: data.results.find(result => result.id === selectedProduct2).description
                      };
                      sendDataToServer(dataset1_id, dataset2_info, null, datasetNumber); // Passer le numéro de dataset
                      updateNotificationCount();
                      showSuccessAlert();
                      updateSelectedProducts(datasetNumber, selectedProducts[`dataset${datasetNumber}`]);
                      resetSelectedProduct(datasetNumber);
                    }
                  });
              } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Attention',
                    text: 'Veuillez sélectionner un produit dans Monoprix et Carrefour'
                  });
                console.log('Veuillez sélectionner un produit dans Monoprix et Carrefour');
              }
            });
            pagesContainer.appendChild(searchButton);
          }       

          // Ajout du bouton de recherche dataset3
          if (datasetNumber === '3') {
            const searchButton = document.createElement('button');
            searchButton.innerText = 'Confirmer';
            searchButton.className = 'btn btn-primary';
            searchButton.addEventListener('click', () => {
              const selectedProduct1 = selectedProducts.dataset1;
              const selectedProduct3 = selectedProducts.dataset3;
              if (selectedProduct1 && selectedProduct3) {
                fetch('/get_dataset1_data/')
                    .then(response => response.json())
                    .then(dataset1Data => {
                      const matchingDataset1Item = dataset1Data.results.find(item =>
                        item.similar_product_in_founa === data.results.find(result => result.id === selectedProduct3).name &&
                        item.prix_produit_founa === data.results.find(result => result.id === selectedProduct3).price &&
                        item.description_produit_founa === data.results.find(result => result.id === selectedProduct3).description
                      );
                    if (matchingDataset1Item) {
                      const message = 'Le produit sélectionné dans Founa est déjà associé à un produit dans Monoprix. Voulez-vous annuler la sélection ?';
                      Swal.fire({
                        title: 'Confirmation',
                        text: message,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: 'Continuer',
                        cancelButtonText: 'Annuler'
                      }).then((result) => {
                        if (result.value) {
                          // L'utilisateur a cliqué sur "Continuer"
                          // Effectuez les actions nécessaires ici
                          const dataset1_id = selectedProduct1;
                          const dataset3_info = {
                            name: data.results.find(result => result.id === selectedProduct3).name,
                            price: data.results.find(result => result.id === selectedProduct3).price,
                            description: data.results.find(result => result.id === selectedProduct3).description
                          };
                          sendDataToServer(dataset1_id, null, dataset3_info, datasetNumber); // Passer le numéro de dataset
                          updateNotificationCount();
                          showSuccessAlert();
                          updateSelectedProducts(datasetNumber, selectedProducts[`dataset${datasetNumber}`]);
                          resetSelectedProduct(datasetNumber);
                        } else {
                          // L'utilisateur a cliqué sur "Annuler"
                          // Réinitialisez la sélection du produit
                          resetSelectedProduct(datasetNumber);
                        }
                      });
                    } else {
                      const dataset1_id = selectedProduct1;
                      const dataset3_info = {
                        name: data.results.find(result => result.id === selectedProduct3).name,
                        price: data.results.find(result => result.id === selectedProduct3).price,
                        description: data.results.find(result => result.id === selectedProduct3).description
                      };
                      sendDataToServer(dataset1_id, null, dataset3_info, datasetNumber); // Passer le numéro de dataset
                      updateNotificationCount();
                      showSuccessAlert();
                      updateSelectedProducts(datasetNumber, selectedProducts[`dataset${datasetNumber}`]);
                      resetSelectedProduct(datasetNumber);
                    }
                  });
              } else {
                Swal.fire({
                    icon: 'warning',
                    title: 'Attention',
                    text: 'Veuillez sélectionner un produit dans Monoprix et Founa'
                  });
                console.log('Veuillez sélectionner un produit dans Monoprix et Founa');
              }
            });
            pagesContainer.appendChild(searchButton);
          }                      

        });
    }
  
    function createProductCheckbox(productId, datasetNumber) {
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'product-checkbox';
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          if (selectedProducts[`dataset${datasetNumber}`]) {
            const checkbox = document.getElementById(`product${datasetNumber}-${selectedProducts[`dataset${datasetNumber}`]}`);
            if (checkbox) {
              checkbox.checked = false;
            }
          }
          selectedProducts[`dataset${datasetNumber}`] = productId;
        } else if (productId === selectedProducts[`dataset${datasetNumber}`]) {
          selectedProducts[`dataset${datasetNumber}`] = null;
        }
        console.log(selectedProducts);
      });
  
      checkbox.id = `product${datasetNumber}-${productId}`;
      return checkbox;
    }

    function updateSelectedProducts(datasetNumber, productId) {
        selectedProducts[`dataset${datasetNumber}`] = productId;
    
        const productCheckbox = document.getElementById(`product${datasetNumber}-${productId}`);
        const productWrapper = productCheckbox.parentNode;
        const checkedMarker = productWrapper.querySelector('.checked-marker');
    
        if (checkedMarker) {
            productWrapper.removeChild(checkedMarker);
        }
    
        if (productId) {
            const marker = document.createElement('div');
            marker.className = 'checked-marker';
            productWrapper.appendChild(marker);
        }
    }
  
    function sendDataToServer(dataset1_id, dataset2_info, dataset3_info, datasetNumber) {
      const data = {
        dataset1_id: dataset1_id,
        dataset2_info: dataset2_info,
        dataset3_info: dataset3_info
      };
  
      fetch('/recommend/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log('Données envoyées avec succès.');
          } else {
            showFailedAlert()
            console.log('Erreur lors de l\'envoi des données.');
          }
        })
        .catch(error => {
          console.error('Erreur lors de l\'envoi des données:', error);
        });
    }
  
    function showSuccessAlert() {
        Swal.fire({
          icon: 'success',
          title: 'Produit enregistré avec succès !'
        });
      }
      
      function showFailedAlert() {
        Swal.fire({
          icon: 'error',
          title: 'Erreur',
          text: 'Produit non enregistré !'
        });
      }

    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  
    function resetSelectedProduct(datasetNumber) {
      selectedProducts[`dataset${datasetNumber}`] = null;
      document.querySelectorAll(`#results${datasetNumber} input[type="checkbox"]`).forEach(checkbox => {
        checkbox.checked = false;
      });
    }
  }); 