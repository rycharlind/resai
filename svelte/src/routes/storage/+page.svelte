<script lang="ts">
	import { onMount } from "svelte";
	import {
		Dropzone,
		Heading,
		Button,
		Listgroup,
		ListgroupItem,
		Spinner,
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
	} from "flowbite-svelte";

	import { v4 as uuidv4 } from "uuid";

	let loading = false;

	let files: File[] = [];
	let value: string[] = [];

	const dropHandle = (event: any) => {
		console.log("dropHandle");
		console.log(event.dataTransfer.items);
		value = [];
		event.preventDefault();
		if (event.dataTransfer.items) {
			[...event.dataTransfer.items].forEach((item, i) => {
				if (item.kind === "file") {
					const file = item.getAsFile();
					value.push(file.name);
					value = value;
				}
			});
		} else {
			[...event.dataTransfer.files].forEach((file, i) => {
				value = file.name;
			});
		}
	};

	const handleChange = (event: any) => {
		files = event.target.files;
		if (files.length > 0) {
			value.push(files[0].name);
			value = value;
		}
	};

	import type { PageData } from "./$types";
	export let data: PageData;
	let { supabase, session } = data;
	$: ({ supabase, session } = data);

	async function uploadFiles() {
		loading = true;
		const { user } = session;

		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			const uuid = uuidv4();
			const fileName = file.name;
			const fileExtension = fileName.slice(
				((fileName.lastIndexOf(".") - 1) >>> 0) + 2
			); // Get the file extension

			const filePath = `${user.id}/${uuid}.${fileExtension}`;

			const { data, error } = await supabase.storage
				.from("resai-storage")
				.upload(filePath, file, {
					cacheControl: "3600",
					upsert: false,
				});

			if (error) {
				console.log(error);
			} else {
				console.log(data);
				console.log(`Uploaded ${file.name}!`);
				await addFileMetaData(file, filePath, user.id);
				console.log(`Added ${file.name} to user_storage!`);
			}
		}
		loading = false;
	}

	async function addFileMetaData(
		file: File,
		filePath: string,
		userId: string
	) {
		try {
			const updates = {
				user_id: userId,
				storage_path: filePath,
				file_name: file.name,
			};

			let { error } = await supabase.from("user_storage").insert(updates);

			if (error) {
				throw error;
			}
		} catch (error) {
			if (error instanceof Error) {
				alert(error.message);
			}
		}
	}

	// This isn't working yet.  But will be the preferred solution in the future.
	async function uploadFilesTut() {
		if (session) {
			loading = true;

			const { user } = session;
			const access_token = session.access_token;

			for (let i = 0; i < files.length; i++) {
				const file = files[i];
				await uploadFileTus(
					`${user.id}/${file.name}`,
					file,
					access_token
				);
			}

			loading = false;
		}
	}

	// https://supabase.com/docs/guides/storage/uploads#resumable-upload

	import * as tus from "tus-js-client";

	// todo: put these in env vars.
	const bucketName = "resapi-storage";
	const projectId = "xutxpdiimpvslejdxtzy";

	async function uploadFileTus(fileName: string, file: File, token: string) {
		console.log(fileName, file, token);
		return new Promise((resolve, reject) => {
			var upload = new tus.Upload(file, {
				endpoint: `https://${projectId}.supabase.co/storage/v1/upload/resumable`,
				retryDelays: [0, 3000, 5000, 10000, 20000],
				headers: {
					authorization: `Bearer ${token}`,
					"x-upsert": "true", // optionally set upsert to true to overwrite existing files
				},
				uploadDataDuringCreation: true,
				metadata: {
					bucketName: bucketName,
					objectName: fileName,
					contentType: "image/png",
					cacheControl: 3600,
				},
				chunkSize: 6 * 1024 * 1024, // NOTE: it must be set to 6MB (for now) do not change it
				onError: function (error) {
					console.log("Failed because: " + error);
					reject(error);
				},
				onProgress: function (bytesUploaded, bytesTotal) {
					var percentage = (
						(bytesUploaded / bytesTotal) *
						100
					).toFixed(2);
					console.log(bytesUploaded, bytesTotal, percentage + "%");
				},
				onSuccess: function () {
					// console.log(upload)
					console.log(
						"Download %s from %s",
						upload.file.name,
						upload.url
					);
					resolve();
				},
			});

			// Check if there are any previous uploads to continue.
			return upload
				.findPreviousUploads()
				.then(function (previousUploads) {
					// Found previous uploads so we select the first one.
					if (previousUploads.length) {
						upload.resumeFromPreviousUpload(previousUploads[0]);
					}

					// Start the upload
					upload.start();
				});
		});
	}

	let storageData: any[] = [];

	async function getUserStorage() {
		try {
			const { user } = session;

			const { data, error, status } = await supabase
				.from("user_storage")
				.select("user_id, storage_path, file_name, created_at")
				.eq("user_id", user.id);

			if (error && status !== 406) throw error;

			if (data) {
				console.log("User Storage Data");
				console.log(data);
				const filePaths = data.map((item) => item.storage_path);
				console.log("File Paths");
				console.log(filePaths);
				const signedUrls = await getSignedStorageUrls(filePaths);
				storageData = mapSignedUrlsToStorageData(signedUrls, data);
				console.log("Final Storage Data");
				console.log(storageData);
			}
		} catch (error) {
			if (error instanceof Error) {
				alert(error.message);
			}
		}
	}

	async function getSignedStorageUrls(filePaths: string[]) {
		try {
			const { data, error } = await supabase.storage
				.from("resai-storage")
				.createSignedUrls(filePaths, 86400);

			if (error) throw error;

			if (data) {
				console.log("Signed Urls Data");
				console.log(data);
				return data;
			}
		} catch (error) {
			if (error instanceof Error) {
				alert(error.message);
			}
		}
	}

	function mapSignedUrlsToStorageData(
		signedUrlItems: any[],
		_storageData: any[]
	) {
		return _storageData.map((item) => {
			const signedUrlItem = signedUrlItems.find(
				(signedUrlItem) => signedUrlItem.path === item.storage_path
			);
			return {
				...item,
				signed_url: signedUrlItem?.signedUrl,
			};
		});
	}

	onMount(async () => {
		getUserStorage();
	});
</script>

<div class="page-body">
	<div class="page-content">
		<Heading
			tag="h1"
			class="mb-4"
			customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl"
			>Storage</Heading
		>

		<Dropzone
			id="dropzone"
			multiple
			on:drop={dropHandle}
			on:dragover={(event) => {
				event.preventDefault();
			}}
			on:change={handleChange}
			style="height: auto; padding: 32px 0px;"
		>
			<svg
				aria-hidden="true"
				class="mb-3 w-10 h-10 text-gray-400"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
				xmlns="http://www.w3.org/2000/svg"
				><path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
				/></svg
			>
			{#if files.length === 0}
				<p class="mb-2 text-sm text-gray-500 dark:text-gray-400">
					<span class="font-semibold">Click to upload</span> or drag and
					drop
				</p>
				<p class="text-xs text-gray-500 dark:text-gray-400">
					PDF, CSV, Excel (Max: 10MB)
				</p>
			{:else}
				<Listgroup items={files} let:item class="mt-2">
					{#if item}
						<ListgroupItem>{item.name}</ListgroupItem>
					{:else}
						<ListgroupItem>No files</ListgroupItem>
					{/if}
				</Listgroup>
			{/if}
		</Dropzone>
		<Button
			style="width:200px; margin-top:16px"
			size="xl"
			disabled={loading}
			on:click={uploadFiles}
		>
			{#if loading}
				<Spinner class="mr-3" size="4" />Saving ...
			{:else}
				Upload
			{/if}
		</Button>

		{#if storageData}
			<Table hoverable={true} style="margin-top:32px">
				<TableHead>
					<TableHeadCell>File Name</TableHeadCell>
					<TableHeadCell>Created At</TableHeadCell>
				</TableHead>
				<TableBody class="divide-y">
					{#each storageData as item}
						<TableBodyRow>
							<TableBodyCell>
								<a
									href={item.signed_url}
									target="_new"
									class="font-medium text-primary-600 hover:underline dark:text-primary-500"
									>{item.file_name}</a
								>
							</TableBodyCell>
							<TableBodyCell>{item.created_at}</TableBodyCell>
						</TableBodyRow>
					{/each}
				</TableBody>
			</Table>
		{/if}
	</div>
</div>
