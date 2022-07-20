db.createUser({
  user: "root",
  pwd: "root",
  roles: [
    {
      role: "readWrite",
      db: "scraped_history",
    },
  ],
});

db = new Mongo().getDB("scraped_history");
db.createCollection("scraped_products", { capped: false });
db.getCollection("scraped_products").createIndex({ url: 1 }, { unique: true });
db.insert({ url: "test" });
