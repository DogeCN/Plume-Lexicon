use serialization::Deserialize;
use std::{
    collections::HashMap,
    fs::File,
    io::{Result, Seek, SeekFrom, copy},
    marker::PhantomData,
    sync::Arc,
};
use xz2::read::XzDecoder;

pub struct DBReader<T> {
    _marker: PhantomData<T>,
    pub name: String,
    pub name_zh: String,
    pub indexes: HashMap<Arc<String>, usize>,
    decoder: Option<XzDecoder<File>>,
    temp: String,
    value: Option<File>,
}

impl<T: Deserialize> DBReader<T> {
    pub fn from(path: &str, temp: &str) -> Result<DBReader<T>> {
        let mut decoder = XzDecoder::new(File::open(&path)?);
        let name = String::deserialize(&mut decoder)?;
        let name_zh = String::deserialize(&mut decoder)?;
        Ok(DBReader::<T> {
            _marker: PhantomData,
            name,
            name_zh,
            indexes: HashMap::new(),
            decoder: Some(decoder),
            temp: temp.to_owned(),
            value: None,
        })
    }

    pub fn load(&mut self) -> Result<()> {
        let mut decoder = self.decoder.take().unwrap();
        for _ in 0..usize::deserialize(&mut decoder)? {
            self.indexes.insert(
                Arc::new(String::deserialize(&mut decoder)?),
                usize::deserialize(&mut decoder)?,
            );
        }
        copy(&mut decoder, &mut File::create(&self.temp)?)?;
        self.value = Some(File::open(&self.temp)?);
        self.decoder = Some(decoder);
        Ok(())
    }

    pub fn get(&mut self, key: &str) -> Option<T> {
        match self.indexes.get(&key.to_owned()) {
            Some(&offset) => self.read(offset as u64).ok(),
            _ => None,
        }
    }

    pub fn len(&self) -> usize {
        self.indexes.len()
    }

    pub fn keys(&self) -> Vec<Arc<String>> {
        self.indexes.keys().cloned().collect()
    }

    pub fn contains(&self, key: &str) -> bool {
        self.indexes.contains_key(&key.to_owned())
    }

    pub fn read(&mut self, offset: u64) -> Result<T> {
        let mut file = self.value.as_ref().unwrap();
        file.seek(SeekFrom::Start(offset))?;
        Ok(T::deserialize(&mut file)?)
    }
}

impl<T> Drop for DBReader<T> {
    fn drop(&mut self) {
        self.value.take();
        let _ = std::fs::remove_file(&self.temp);
    }
}
