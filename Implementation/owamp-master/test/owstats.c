/*
 *        File:         owstats.c
 *
 *        Author:       Erik Reid
 *                      GÉANT
 *
 *        Description:  Basic session parsing & statistics sanity check
 */
#include <owamp/owamp.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>

#include <I2util/util.h>

#include "./owtest_utils.h"


// reference session from a 100-packet test
#define EXPECTED_NUM_RECORDS 100
#define SESSION_DATA \
    "4f7741000000000300000001000000640000000000000064000000000000" \
    "00b800000000000000b801040001000000010000006423f222667f000001" \
    "0000000000000000000000007f0000010000000000000000000000007f00" \
    "0001dd12e59ff0d341db48dee1c400000000dd12e5a10573197d00000002" \
    "0a5119ce0000000000000000000000000000000000000000000000000000" \
    "0000000000000000000000000000199999a0000000000000000000000000" \
    "000000000000000092d792d7dd12e5a1115e2e9add12e5a111661ca5ff00" \
    "00000192d792d7dd12e5a173bef229dd12e5a173cd2ad1ff0000000292d7" \
    "92d7dd12e5a18e289f6cdd12e5a18e349da7ff0000000392d792d7dd12e5" \
    "a1a6298a4edd12e5a1a62e20b5ff0000000492d792d7dd12e5a1be6d5eb9" \
    "dd12e5a1be78f84aff0000000592d792d7dd12e5a1ea5b58fddd12e5a1ea" \
    "654f20ff0000000692d792d7dd12e5a20264a75add12e5a2026d5eb9ff00" \
    "00000792d792d7dd12e5a21ed5b6ebdd12e5a21edf4864ff0000000892d7" \
    "92d7dd12e5a23e57c11cdd12e5a23e612040ff0000000992d792d7dd12e5" \
    "a25a767da0dd12e5a25a846265ff0000000a92d792d7dd12e5a2618a5d51" \
    "dd12e5a261966c53ff0000000b92d792d7dd12e5a28b8c7e93dd12e5a28b" \
    "949ef3ff0000000c92d792d7dd12e5a2b0659d7edd12e5a2b06f614cff00" \
    "00000d92d792d7dd12e5a2b69b526bdd12e5a2b6a92669ff0000000e92d7" \
    "92d7dd12e5a2bf7907bedd12e5a2bf82a9feff0000000f92d792d7dd12e5" \
    "a2d469adaedd12e5a2d472437eff0000001092d792d7dd12e5a3070b8abc" \
    "dd12e5a307157018ff0000001192d792d7dd12e5a31004f8d1dd12e5a310" \
    "1107d3ff0000001292d792d7dd12e5a31defb49ddd12e5a31df85b34ff00" \
    "00001392d792d7dd12e5a33003fd29dd12e5a33006ce95ff0000001492d7" \
    "92d7dd12e5a370558404dd12e5a370595118ff0000001592d792d7dd12e5" \
    "a3836b6bcddd12e5a3836e6f8eff0000001692d792d7dd12e5a384aed75d" \
    "dd12e5a384b07acbff0000001792d792d7dd12e5a38e3ead28dd12e5a38e" \
    "415d06ff0000001892d792d7dd12e5a3971dc2cddd12e5a397216e53ff00" \
    "00001992d792d7dd12e5a39b4903c3dd12e5a39b4bf6bdff0000001a92d7" \
    "92d7dd12e5a3c8b2c5ffdd12e5a3c8b69313ff0000001b92d792d7dd12e5" \
    "a40193d2f4dd12e5a40196720bff0000001c92d792d7dd12e5a41e80d5fa" \
    "dd12e5a41e843e64ff0000001d92d792d7dd12e5a48cacc719dd12e5a48c" \
    "b00df5ff0000001e92d792d7dd12e5a4a0d05d20dd12e5a4a0d3501aff00" \
    "00001f92d792d7dd12e5a4b92732f0dd12e5a4b92b0004ff0000002092d7" \
    "92d7dd12e5a4b9c3d47cdd12e5a4b9c78002ff0000002192d792d7dd12e5" \
    "a4ca5f480add12e5a4ca6336acff0000002292d792d7dd12e5a4cc74f0e9" \
    "dd12e5a4cc787ae1ff0000002392d792d7dd12e5a4f056cb64dd12e5a4f0" \
    "591698ff0000002492d792d7dd12e5a4fd910a24dd12e5a4fd9ca3b5ff00" \
    "00002592d792d7dd12e5a50e7a215ddd12e5a50e7d6839ff0000002692d7" \
    "92d7dd12e5a5749b0feadd12e5a5749eaaa9ff0000002792d792d7dd12e5" \
    "a5970404a0dd12e5a597073ab6ff0000002892d792d7dd12e5a5a8378353" \
    "dd12e5a5a83c6d9dff0000002992d792d7dd12e5a5ac9cb358dd12e5a5ac" \
    "9ffa35ff0000002a92d792d7dd12e5a5ad00f87cdd12e5a5ad039793ff00" \
    "00002b92d792d7dd12e5a5b817fd7cdd12e5a5b81b8774ff0000002c92d7" \
    "92d7dd12e5a5ec1ffc4edd12e5a5ec23eaf0ff0000002d92d792d7dd12e5" \
    "a6b5a9d8dfdd12e5a6b5acfe2dff0000002e92d792d7dd12e5a6c0175336" \
    "dd12e5a6c01b204aff0000002f92d792d7dd12e5a6ca0ab599dd12e5a6ca" \
    "0e71e6ff0000003092d792d7dd12e5a6e9d09435dd12e5a6e9d40d66ff00" \
    "00003192d792d7dd12e5a6ea4a79d4dd12e5a6ea4d7d94ff0000003292d7" \
    "92d7dd12e5a72c940a97dd12e5a72c981ac7ff0000003392d792d7dd12e5" \
    "a7a54cda56dd12e5a7a54f796dff0000003492d792d7dd12e5a7c25ff917" \
    "dd12e5a7c263830fff0000003592d792d7dd12e5a7d95096a3dd12e5a7d9" \
    "5463b8ff0000003692d792d7dd12e5a7e70d400ddd12e5a7e711503dff00" \
    "00003792d792d7dd12e5a7e877130fdd12e5a7e879c2edff0000003892d7" \
    "92d7dd12e5a7ebf3df12dd12e5a7ebf6f39aff0000003992d792d7dd12e5" \
    "a7ef734a2ddd12e5a7ef780222ff0000003a92d792d7dd12e5a7f698dbb7" \
    "dd12e5a7f69d3fc9ff0000003b92d792d7dd12e5a7f724732fdd12e5a7f7" \
    "255e11ff0000003c92d792d7dd12e5a7f7a97cefdd12e5a7f7aa67d0ff00" \
    "00003d92d792d7dd12e5a8016ffaeddd12e5a80173a673ff0000003e92d7" \
    "92d7dd12e5a802b56e94dd12e5a802b92ae2ff0000003f92d792d7dd12e5" \
    "a811aa8422dd12e5a811af8ffbff0000004092d792d7dd12e5a82284e1d1" \
    "dd12e5a82288e13aff0000004192d792d7dd12e5a827695731dd12e5a827" \
    "6e8497ff0000004292d792d7dd12e5a856364defdd12e5a85638cb78ff00" \
    "00004392d792d7dd12e5a861d78a15dd12e5a861db359bff0000004492d7" \
    "92d7dd12e5a866afdfacdd12e5a866b4a868ff0000004592d792d7dd12e5" \
    "a873972677dd12e5a8739bfffbff0000004692d792d7dd12e5a8789a0478" \
    "dd12e5a8789ce6abff0000004792d792d7dd12e5a87e232afddd12e5a87e" \
    "262ebdff0000004892d792d7dd12e5a89215aae2dd12e5a8921945a1ff00" \
    "00004992d792d7dd12e5a8aaa3bfe3dd12e5a8aaa63d6bff0000004a92d7" \
    "92d7dd12e5a8c71d6266dd12e5a8c7205560ff0000004b92d792d7dd12e5" \
    "a8cc88b749dd12e5a8cc8c4141ff0000004c92d792d7dd12e5a8cf9e18da" \
    "dd12e5a8cfa12d61ff0000004d92d792d7dd12e5a8dafae995dd12e5a8da" \
    "ff90c4ff0000004e92d792d7dd12e5a901429378dd12e5a90146a3a8ff00" \
    "00004f92d792d7dd12e5a943a7d1d6dd12e5a943ab2979ff0000005092d7" \
    "92d7dd12e5a95df433aedd12e5a95df82250ff0000005192d792d7dd12e5" \
    "a98dd4e02cdd12e5a98dd8057aff0000005292d792d7dd12e5aa510aaa6c" \
    "dd12e5aa510d7bd8ff0000005392d792d7dd12e5aa5b5019e2dd12e5aa5b" \
    "586c97ff0000005492d792d7dd12e5aa6e0e1f6cdd12e5aa6e120e0eff00" \
    "00005592d792d7dd12e5aa6f3a57d9dd12e5aa6f3df298ff0000005692d7" \
    "92d7dd12e5aaae3e7d02dd12e5aaae4206faff0000005792d792d7dd12e5" \
    "aac3e6d57bdd12e5aac3eaf672ff0000005892d792d7dd12e5aadd056c3f" \
    "dd12e5aadd096ba8ff0000005992d792d7dd12e5ab0ca468bbdd12e5ab0c" \
    "a889b2ff0000005a92d792d7dd12e5ab1f801e59dd12e5ab1f845017ff00" \
    "00005b92d792d7dd12e5ab6500d09bdd12e5ab6503c395ff0000005c92d7" \
    "92d7dd12e5abbb4e92c6dd12e5abbb524f13ff0000005d92d792d7dd12e5" \
    "abc9da1114dd12e5abc9dd4729ff0000005e92d792d7dd12e5ac026af780" \
    "dd12e5ac026ea307ff0000005f92d792d7dd12e5ac0e0c95d8dd12e5ac0e" \
    "1062ecff0000006092d792d7dd12e5ac19261860dd12e5ac192a0702ff00" \
    "00006192d792d7dd12e5acb8b9c3a3dd12e5acb8bdb245ff0000006292d7" \
    "92d7dd12e5acbf805efedd12e5acbf857b9dff0000006392d792d7dd12e5" \
    "acc963e54add12e5acc9671b60ff"


/*
 * Function:        main
 *
 * Description:     parse a reference session data set, parse
 *                  and compute standard statistics
 *
 * In Args:         argc, argv (unused)
 *
 * Out Args:
 *
 * Scope:           unit test (run using make check)
 * Returns:         non-zero in case of error
 * Side Effect:
 */
int
main(
        int     argc    __attribute__((unused)),
        char    **argv
    ) {

    int test_result = 1; // default is to fail

    OWPStats stats = NULL;
    OWPContext ctx = tmpContext(argv);
    OWPSessionHeaderRec hdr;

    FILE *fp = tmpSessionDataFile(SESSION_DATA);

    int num_rec = OWPReadDataHeader(ctx,fp,&hdr);

    if (num_rec != EXPECTED_NUM_RECORDS) {
        printf("expected %d records, found %d\n",
            EXPECTED_NUM_RECORDS, num_rec);
        goto done;
    }

    if (!hdr.header) {
        printf("header data not initialized\n");
        goto done;
    }

    stats = OWPStatsCreate(
        ctx, fp, &hdr, "source", "destination", 'm', 0.0001);
    if (!stats) {
        printf("OWPStatsCreate failed\n");
        goto done;
    }

    if (!OWPStatsParse(stats, NULL, 0, 0, ~0)) {
        printf("OWPStatsParse failed\n");
        goto done;
    }

    OWPStatsPrintSummary(stats, stdout, NULL, 0);

    // no errors: set test_result to passed
    test_result = 0;

done:
    fclose(fp);
    OWPContextFree(ctx);
    if(stats) {
        OWPStatsFree(stats);
    }
    exit(test_result);
}

