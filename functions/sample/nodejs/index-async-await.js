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
         let dbList = await cloudant.db.list();
         console.log(dbList)
         return { "dbs": dbList };
     } catch (error) {
         console.log(error)
         return { error: error.description };
     }
 
 }

main({})
