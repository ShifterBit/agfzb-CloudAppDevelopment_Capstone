/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: process.env.COUCH_URL,
         plugins: { iamauth: { iamApiKey: process.env.IAM_API_KEY } }
     });
 
 
     try {
         let dealership_db = cloudant.use("dealerships")
         let dealership_list;
         const q = {
           selector: {
             st: { "$eq": params.state },
           },
         };
         if (params.state === undefined) {
          dealership_list = await dealership_db.list({include_docs: true})
          } else {
          dealership_list = await dealership_db.find(q);
          }


         return { dealership_list };
     } catch (error) {
         console.log(error)
         return { error: error.description };
     }
 
 }

main({})

