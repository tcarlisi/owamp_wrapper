/*
 **      $Id$
 */
/************************************************************************
 *                                                                      *
 *                             Copyright (C)  2002                      *
 *                                Internet2                             *
 *                             All Rights Reserved                      *
 *                                                                      *
 ************************************************************************/
/*
 **        File:        error.c
 **
 **        Author:      Jeff W. Boote
 **                     Anatoly Karp
 **
 **        Date:        Fri Mar 29 15:36:44  2002
 **
 **        Description:        
 */
#include <owampP.h>

#include <stdio.h>
#include <stdarg.h>

void
OWPError_(
        OWPContext      ctx,
        OWPErrSeverity  severity,
        OWPErrType      etype,
        const char      *fmt,
        ...
        )
{
    va_list                ap;

    va_start(ap,fmt);

    if(ctx && ctx->eh){
        I2ErrLogVT(ctx->eh,(int)severity,etype,fmt,ap);
    }
    else{
        char    buff[_OWP_ERR_MAXSTRING];

        vsnprintf(buff,sizeof(buff),fmt,ap);
        fwrite(buff,sizeof(char),strlen(buff),stderr);
        fwrite("\n",sizeof(char),1,stderr);
    }
    va_end(ap);

    return;
}

int
OWPReportLevelByName(
        const char      *name
        )
{
    if(!strncasecmp(name,"fatal",6)){
        return (int) OWPErrFATAL;
    }
    else if(!strncasecmp(name,"warning",8)){
        return (int) OWPErrWARNING;
    }
    else if(!strncasecmp(name,"info",5)){
        return (int) OWPErrINFO;
    }
    else if(!strncasecmp(name,"debug",6)){
        return (int) OWPErrDEBUG;
    }
    else if(!strncasecmp(name,"all",4)){
        return (int) OWPErrOK;
    }
    else if(!strncasecmp(name,"none",5)){
        return 0;
    }
    
    return -1;
}
