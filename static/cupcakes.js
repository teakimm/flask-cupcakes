"use strict";

const $cupcakeList = $(".cupcake-list");
const $form = $("#cupcake-form");

/** Returns an array of cupcakes from calling cupcake api */
async function getCupcakes() {
  const response = await fetch(`/api/cupcakes`);

  const cupcakeData = await response.json();

  return cupcakeData.cupcakes;
}

/**Returns a jquery object of a cupcake list item given a cupcake object */
function createCupcakeHTML(cupcake) {
  return $(`
    <div id=${cupcake.id}>
      <li>
        <p>Flavor: ${cupcake.flavor}</p>
        <p>Size: ${cupcake.size}</p>
        <p>Rating: ${cupcake.rating}</p>
      </li>
      <img src="${cupcake.image_url}"
    </div>
  `);
}

/** Controller function that renders of all cupcakes in the database */
async function renderCupcakes() {
  const cupcakes = await getCupcakes();

  for (let cupcake of cupcakes) {
    const $cupcakeHTML = createCupcakeHTML(cupcake);
    $cupcakeList.append($cupcakeHTML);
  }
}

/** Makes a post request with the body being the user's form inputs
 * returns an object of the created cupcake
 */
async function createCupcake() {
  const response = await fetch(`/api/cupcakes`, {
    method: "POST",
    body: JSON.stringify({
      "flavor": $("#flavor").val(),
      "size": $("#size").val(),
      "rating": $("#rating").val(),
      "image_url": $("#image_url").val() || null
    }),
    headers: {
      "Content-Type": "application/json"
    }
  });
  return await response.json();
}

/** Controller function that makes the cupcake when submitted and renders
 * the cupcake in the HTML
 */
async function submitAndRenderCupcake(evt) {
  evt.preventDefault();

  const cupcakeData = await createCupcake();

  const $newCupcake = createCupcakeHTML(cupcakeData.cupcake);
  $cupcakeList.append($newCupcake);
}

$form.on("submit", submitAndRenderCupcake);

renderCupcakes();