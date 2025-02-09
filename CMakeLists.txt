cmake_minimum_required(VERSION 3.28)
project(mujoco_wasm LANGUAGES CXX)

add_subdirectory(dependencies)

# TODO: --emit-tsd mujoco_wasm.d.ts causes 
# BindingError: Missing binding for type: 'P8mjModel_'
set(EMCC_LINKER_FLAGS
    "-s ASSERTIONS=1 --bind -s ALLOW_MEMORY_GROWTH=1 -s EXPORT_ES6=1 -s MODULARIZE=1 -s FORCE_FILESYSTEM=1 -s EXPORTED_RUNTIME_METHODS=['FS','MEMFS'] -s EXPORT_NAME=load_mujoco -s EXCEPTION_CATCHING_ALLOWED=['load_from_xml']"
)

add_executable(mujoco_wasm)
target_sources(mujoco_wasm PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/main.genned.cc)
target_compile_features(mujoco_wasm PRIVATE cxx_std_20)
set_target_properties(mujoco_wasm PROPERTIES LINK_FLAGS "${EMCC_LINKER_FLAGS}")
target_link_libraries(mujoco_wasm PRIVATE mujoco)

install(FILES "$<TARGET_FILE_DIR:mujoco_wasm>/mujoco_wasm.js"
              "$<TARGET_FILE_DIR:mujoco_wasm>/mujoco_wasm.wasm"
        DESTINATION ${CMAKE_SOURCE_DIR}/dist)
