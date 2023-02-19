

const $submitForm = $("#submit-form");
const $allCupcakesList = $("#all-cupcakes-list");

// This is the global list of the cupcakes, an instance of cupcakeList
let cupcakeList;

/** Handle submit button in submit form. */
async function submitNewCupcake(evt) {
    console.log("submitNewCupcake", evt);
    evt.preventDefault();
  
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
  
    const newCupcake = await cupcakeList.addCupcake( {flavor, size, rating, image});

    $submitForm.trigger("reset");

    putCupcakesOnPage();
  }
  
$submitForm.on("submit", submitNewCupcake);


/** Handle delete button for deleting particular cupcake */

async function deleteCupcake() {

    const id = $(this).data('id');
    const response = await cupcakeList.deleteCupcake(id);

    putCupcakesOnPage();
}

$allCupcakesList.on("click", ".delete-cupcake", deleteCupcake)


/** Handle search button to put searched list of cupcakes in page */
$('#search-btn').click(searchCupcakes)

async function searchCupcakes() {
    const search = $('#search').val();
    cupcakeList = await CupcakeList.searchCupcakes(search);
    putCupcakesOnPage();
}


function putCupcakesOnPage() {
    $allCupcakesList.empty();

    // loop through all of our stories and generate HTML for them
    for (let cupcake of cupcakeList.cupcakes) {
        const $cupcake = generateStoryMarkup(cupcake);
        $allCupcakesList.append($cupcake);
    }

    $allCupcakesList.show();
}

function generateStoryMarkup(cupcake) {
    return $(`
        <li id="${cupcake.id}">
            <img class="thumb-nail" src="${cupcake.image}">
            <p class="story-user">Flavor: ${cupcake.flavor}</p>
            <p class="story-hostname">Size: ${cupcake.size}</p>
            <p class="story-author">Rating: ${cupcake.rating}</p>
            <form>
                <button class="delete-cupcake btn-sm btn-danger" data-id="${cupcake.id}" >Delete</button>
                <button class="edit-cupcake btn-sm btn-success" data-id="${cupcake.id}" formaction="/api/cupcakes/${cupcake.id}/edit" >Edit</button>
            </form>
        </li>
    `);
}

async function getAndShowCupcakesonStart() {
    cupcakeList = await CupcakeList.fetchAllCupcakes();
    putCupcakesOnPage();
}


async function start() {
    await getAndShowCupcakesonStart();
}

$(start)
