module.exports = {
    async up(knex)
    {
        return knex.schema.createTable("chemicals", t => {
            t.string("id").primary().notNullable();
            t.string("substance").notNullable();
            t.string("identifier").notNullable();
            t.string("scope").notNullable();
            t.string("threshold").notNullable();
            t.string("exemptions").notNullable();
            t.string("reference").notNullable();
        });
    },
    async down(knex)
    {
        return knex.schema.dropTable("chemicals");
    }
}



