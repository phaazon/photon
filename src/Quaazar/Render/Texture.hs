-----------------------------------------------------------------------------
-- |
-- Copyright   : (C) 2014 Dimitri Sabadie
-- License     : BSD3
--
-- Maintainer  : Dimitri Sabadie <dimitri.sabadie@gmail.com>
-- Stability   : experimental
-- Portability : portable
--
----------------------------------------------------------------------------

module Quaazar.Render.Texture where

import Control.Monad.Trans ( MonadIO(..) )
import Numeric.Natural ( Natural )
import Quaazar.Core.Texture ( TexelFormat(..), Texture(..) )
import Quaazar.Render.GL.GLObject
import qualified Quaazar.Render.GL.Texture as GL

newtype GPUTexture = GPUTexture { bindTextureAt :: Natural -> IO () }

gpuTexture :: (MonadIO m)
           => Texture
           -> GL.Wrap
           -> GL.Filter
           -> m GPUTexture
gpuTexture (Texture width height format texels) wrap flt = liftIO $ do
    tex <- genObject :: IO GL.Texture2D
    GL.bindTextureAt tex 0
    GL.setTextureWrap tex wrap
    GL.setTextureFilters tex flt
    GL.setTextureImage tex ift width height ft texels
    return . GPUTexture $ GL.bindTextureAt tex
  where
    (ft,ift) = case format of
      R -> (GL.R,GL.R32F)
      RG -> (GL.RG,GL.RG32F)
      RGB -> (GL.RGB,GL.RGB32F)
      RGBA -> (GL.RGBA,GL.RGBA32F)