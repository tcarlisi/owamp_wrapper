/*
 *      $Id$
 */
/************************************************************************
 *                                                                      *
 *                             Copyright (C)  2003                      *
 *                                Internet2                             *
 *                             All Rights Reserved                      *
 *                                                                      *
 ************************************************************************/
/*
 *        File:         owtvec.c
 *
 *        Author:       Jeff W. Boote
 *                      Internet2
 *
 *        Date:         Mon Oct 20 13:55:38 MDT 2003
 *
 *        Description:        
 */
#include <owamp/owamp.h>
#include <I2util/util.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <assert.h>
#include <inttypes.h>

int
main(
        int     argc    __attribute__((unused)),
        char    **argv
    ) {
    char                *progname;
    I2LogImmediateAttr  ia;
    I2ErrHandle         eh;
    OWPContext          ctx;
    uint8_t             seed[16];
    char                *seedvals[4] = {
        "2872979303ab47eeac028dab3829dab2",
        "0102030405060708090a0b0c0d0e0f00",
        "deadbeefdeadbeefdeadbeefdeadbeef",
        "feed0feed1feed2feed3feed4feed5ab"};
    char                *expected_sums[4] = {
        "000f4479bd317381",
        "000f433686466a62",
        "000f416c8884d2d3",
        "000f3f0b4b416ec8"};
    unsigned int        nice[] = {1,10,100,1000,100000,1000000};
    unsigned int        i,j,n;
    OWPExpContext       exp;
    OWPNum64            eval;
    OWPNum64            sum;


    ia.line_info = (I2NAME | I2MSG);
#ifndef        NDEBUG
    ia.line_info |= (I2LINE | I2FILE);
#endif
    ia.fp = stderr;

    progname = (progname = strrchr(argv[0], '/')) ? progname+1 : *argv;

    /*
     * Start an error logging session for reporing errors to the
     * standard error
     */
    eh = I2ErrOpen(progname, I2ErrLogImmediate, &ia, NULL, NULL);
    if(! eh) {
        fprintf(stderr, "%s : Couldn't init error module\n", progname);
        exit(1);
    }

    /*
     * Initialize library with configuration functions.
     */
    if( !(ctx = OWPContextCreate(eh))){
        I2ErrLog(eh, "Unable to initialize OWP library.");
        exit(1);
    }

    for(i=0;i<I2Number(seedvals);i++){
        assert(I2HexDecode(seedvals[i],seed,16));
        assert((exp = OWPExpContextCreate(ctx,(uint8_t *)seed)));
        fprintf(stdout,"SEED = 0x%s\n",seedvals[i]);
        n = 0;
        sum = OWPULongToNum64(0);
        for(j=1;j<=1000000;j++){
            eval = OWPExpContextNext(exp);
            sum = OWPNum64Add(sum,eval);
            if((n < I2Number(nice)) && (j == nice[n])){
                /* hex encoded big-endian ov eval and sum */
                char                ve[17];
                char                vs[17];
                sprintf(ve, "%016" PRIx64, eval);
                sprintf(vs, "%016" PRIx64, sum);
                fprintf(stdout,
                        "EXP[%d] = 0x%s (%f)\tSUM[%d] = 0x%s (%f)\n",
                        j,ve,OWPNum64ToDouble(eval),
                        j,vs,OWPNum64ToDouble(sum));
                n++;
            }
        }
        OWPExpContextFree(exp);
        exp = NULL;

        char sum_hex[17];
        sprintf(sum_hex, "%016" PRIx64, sum);
        fprintf(stdout,
                "FINAL SUM[%d]: 0x%s, EXPECTED_SUM[%d]: 0x%s\n",
                i, sum_hex, i, expected_sums[i]);
        if(strcmp(sum_hex, expected_sums[i])) {
            fprintf(stdout, "sum validation error");
            exit(1);
        }

        fprintf(stdout,"\n");
    }

    exit(0);
}
