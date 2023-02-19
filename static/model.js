/**************************************
 * 
 * Cupcake class
 * 
***************************************/
class Cupcake {
    /** Make instance of Cupcake from data object about cupcake:
     *   - {id, flavor, size, rating, image}
     */

    constructor({id, flavor, size, rating, image}) {
        this.id = id;
        this.flavor = flavor;
        this.size = size;
        this.rating = rating;
        this.image = image;
    }
}

/**************************************
 * 
 * List of cupcake instances: used by UI to show cupcake lists in DOM.
 * 
***************************************/

class CupcakeList {
    constructor(cupcakes) {
        this.cupcakes = cupcakes;
    }

    /* Generate a new CupcakeList. It:
       - calls the API
       - builds an array of Cupcake instances
       - makes a single CupcakeList instance out of that
       - returns the StoryList instance
    */

    static async fetchAllCupcakes() {

        // query the /api/cupcakes endpoint 
        const response = await axios.get(`/api/cupcakes`)

        // turn plain old story objects from API into instances of Cupcake class
        const cupcakeList = response.data.cupcakes.map(cupcake => new Cupcake(cupcake));
        
        return new CupcakeList(cupcakeList);
    }

    static async searchCupcakes(search) {
        // send get request with query string to API
        const response = await axios.get(`/api/cupcakes/search`, { params: { search: search } });

        // turn plain old story objects from API into instances of Cupcake class
        const cupcakeList = response.data.cupcakes.map(cupcake => new Cupcake(cupcake));

        return new CupcakeList(cupcakeList);
    }

    async addCupcake(newCupcake) {
        // send post request to API
        const response = await axios.post(`/api/cupcakes`, newCupcake);

        const cupcake = new Cupcake(response.data.cupcake);
        this.cupcakes.push(cupcake);
        return cupcake;
    }

    async deleteCupcake(id) {
        // send delete request to API
        const response = await axios.delete(`/api/cupcakes/${id}`);

        this.cupcakes = this.cupcakes.filter( cupcake => {
            if(cupcake.id !== id) {
                return cupcake;
            }
        });
        return response.data.message;
    }

    async updateCupcake(id, cupcake) {
        // send delete request to API
        const response = await axios.patch(`/api/cupcakes/${id}/edit`, cupcake);

        
        return response.data;
    }
}